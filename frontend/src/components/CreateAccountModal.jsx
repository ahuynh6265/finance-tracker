import {useState} from "react"
import {createAccount} from "../api/api"

function CreateAccountModal({onCreated, onClose}) {
  const [bank_name, setBank] = useState("")
  const [account_type, setType] = useState("checking")
  const [balance, setBalance] = useState(0)

  function handleCreate() {
    createAccount({bank_name: bank_name, account_type: account_type, balance: balance}).then(() => {
      onCreated()
    }).catch(err => console.error(err))
  }

  return (
  <div className = "modal-overlay">
    <div className = "modal-content">
      <h1 className = "absolute top-4 left-4 text-gray-300 text-xl font-semibold">Create New Account</h1>
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

      <button className = "text-white font-semibold" onClick = {handleCreate}>Create Account</button>
    </div>
  </div>
  )
}
export default CreateAccountModal