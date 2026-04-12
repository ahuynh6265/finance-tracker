import {useState} from "react"
import {fundGoal, withdrawGoal} from "../api/api"

function GoalFundWithdrawModal({goal, mode, accounts, onSuccess, onClose}) {
  const [error, setError] = useState("")
  const [account_id, setAccountID] = useState("")
  const [amount, setAmount] = useState(0)

  function handleSubmit() {
    setError("")
    if (isNaN(Number(amount))) {
      setError("Please enter a numerical value.")
    }
    else if (mode === "fund"){
      fundGoal(goal.id, {account_id: Number(account_id), amount: Number(amount)}).then(() => {
        onSuccess()
      }).catch(err => {
        if (err.response) {
          if (err.response.status === 422) {
            const getError = err.response.data.detail[0].msg
            setError(getError.split(",")[1].trim())
          }
          else {
            setError(err.response.data.detail)
          }
        }
        else {
          setError("Something went wrong.")
        }
      })
    }
    else {
      withdrawGoal(goal.id, {account_id: Number(account_id), amount: Number(amount)}).then(() => {
        onSuccess()
      }).catch(err => {
        if (err.response) {
          if (err.response.status === 422) {
            const getError = err.response.data.detail[0].msg
            setError(getError.split(",")[1].trim())
          }
          else {
            setError(err.response.data.detail)
          }
        }
        else {
          setError("Something went wrong.")
        }
      })
    }
  }
  return (
    <div className = "modal-overlay">
      <div className = "modal-content">
        {(mode === "fund") ? (<h1 className = "absolute top-4 left-4 text-gray-300 text-xl font-semibold">Fund Goal</h1>) : (<h1 className = "absolute top-4 left-4 text-gray-300 text-xl font-semibold">Withdraw from Goal</h1>)}
        <button className = "absolute top-4 right-4 text-white font-semibold" onClick = {onClose}>Close</button>

        <div className = "flex gap-4">
          <div className = "w-full">
            <select className = "modal-input" value = {account_id} onChange = {(e) => setAccountID(e.target.value)}>
              <option value="">Select Account</option>
              {accounts.map (account => 
                <option key = {account.id} value = {account.id}>{account.bank_name}</option>
              )}
            </select>
            <input className = "modal-input" placeholder = "amount" value = {amount} onChange = {(e) => setAmount(e.target.value)}></input>
          </div>
        </div>

        {(mode === "fund") ? (<button className = "text-white font-semibold" onClick = {handleSubmit}>Fund</button>) : (<button className = "text-white font-semibold" onClick = {handleSubmit}>Withdraw</button>)}
        <div className = "text-red-400">{error}</div>
      </div>
    </div>
  )
}
export default GoalFundWithdrawModal 