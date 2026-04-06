import {useState} from "react"
import {createAccount, updateAccount} from "../api/api"

function AccountModal({account, onSuccess, onClose}) {
  const [error, setError] = useState("")

  const [bank_name, setBank] = useState(account ? account.bank_name : "")
  const [account_type, setType] = useState(account ? account.account_type : "checking")
  const [balance, setBalance] = useState(account ? account.balance : 0)

  function handleSubmit() {
    setError("")
    if (account === null) {
      createAccount({bank_name: bank_name, account_type: account_type, balance: Number(balance)}).then(() => {
        onSuccess()
      }).catch(err => {
        if (err.response){
          if (err.response.status === 422) {
            const getError = err.response.data.detail[0].msg 
            setError(getError.split(",")[1].trim())
          }
          else {
            (setError(err.response.data.detail))
          }
        }
        else {
          setError ("Something went wrong.")
        }
      })
    }
    else {
      updateAccount(account.id, {bank_name: bank_name, account_type: account_type, balance: Number(balance)}).then(() => {
        onSuccess()
      }).catch(err => {
        if (err.response){
          if (err.response.status === 422) {
            const getError = err.response.data.detail[0].msg 
            setError(getError.split(",")[1].trim())
          }
          else {
            (setError(err.response.data.detail))
          }
        }
        else {
          setError ("Something went wrong.")
        }
      })
    }
  }

  return (
    <div className = "modal-overlay">
      <div className = "modal-content">
        {account ? (<h1 className = "absolute top-4 left-4 text-gray-300 text-xl font-semibold">Edit Bank Account</h1>) : ( <h1 className = "absolute top-4 left-4 text-gray-300 text-xl font-semibold">Create New Account</h1>)}
        <button className = "absolute top-4 right-4 text-white font-semibold" onClick = {onClose}>Close</button>

        <div className = "flex gap-4">
          <div className = "w-full">
            <input className = "modal-input" placeholder = "Enter Bank Name" value = {bank_name} onChange = {(e) => setBank(e.target.value)}></input>
          </div>
        </div>

        <div className = "flex gap-4">
          <div className = "w-full">
            <h2 className = "text-white font-semibold">Select Account Type</h2>
            <select className = "modal-input" value = {account_type} onChange = {(e) => setType(e.target.value)}>
            <option value = "checking">Checking</option> 
            <option value = "savings">Saving</option> 
            <option value = "credit">Credit</option> 
            </select>
          </div>
          <div className = "w-full">
            <h2 className = "text-white font-semibold">Enter Balance</h2>
            <input className = "modal-input" value = {balance} onChange = {(e) => setBalance(e.target.value)}></input> 
          </div>
        </div>

        {account ? (<button className = "text-white font-semibold" onClick = {handleSubmit}>Save Changes</button>) : (<button className = "text-white font-semibold" onClick = {handleSubmit}>Create Account</button>)}
        <div className = "text-red-400">{error}</div>
      </div>
    </div>
  )
}
export default AccountModal