import {useState} from "react"
import {fundGoal, withdrawGoal, handleAPIError} from "../api/api"

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
      }).catch(err => {setError(handleAPIError(err))})
    }
    else {
      withdrawGoal(goal.id, {account_id: Number(account_id), amount: Number(amount)}).then(() => {
        onSuccess()
      }).catch(err => {setError(handleAPIError(err))})
    }
  }
  return (
    <div className = "modal-overlay">
      <div className = "modal-content">
        {(mode === "fund") ? (<h1 className = "absolute top-4 left-4 text-white text-xl font-semibold">Fund Goal</h1>) : (<h1 className = "absolute top-4 left-4 text-white text-xl font-semibold">Withdraw from Goal</h1>)}
        <button className = "absolute top-4 right-4 text-white font-semibold" onClick = {onClose}>Close</button>

        <div className = "flex gap-4">
          <div className = "w-full flex flex-col gap-3">
            <div>
              <h2 className = "text-white font-semibold">Select Account</h2>
              <select className = "modal-input" value = {account_id} onChange = {(e) => setAccountID(e.target.value)}>
                <option value="">Select Account</option>
                {accounts.map (account =>
                  <option key = {account.id} value = {account.id}>{account.bank_name}</option>
                )}
              </select>
            </div>
            <div>
              <h2 className = "text-white font-semibold">Enter Amount</h2>
              <input className = "modal-input" placeholder = "Enter Amount" value = {amount} onChange = {(e) => setAmount(e.target.value)}></input>
            </div>
          </div>
        </div>

        {(mode === "fund") ? (<button className = "bg-white text-purple-600 hover:bg-gray-100 font-semibold px-6 py-2 rounded-lg shadow-sm transition-colors" onClick = {handleSubmit}>Fund</button>) : (<button className = "bg-white text-purple-600 hover:bg-gray-100 font-semibold px-6 py-2 rounded-lg shadow-sm transition-colors" onClick = {handleSubmit}>Withdraw</button>)}
        <div className = "text-red-400">{error}</div>
      </div>
    </div>
  )
}
export default GoalFundWithdrawModal 