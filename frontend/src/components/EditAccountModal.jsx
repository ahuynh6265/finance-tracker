import {useState} from "react"
import {updateAccount} from "../api/api"

function EditAccountModal({account, onUpdated, onClose}) {
  const [newBank, setNewBank] = useState(account.bank_name)
  const [newAccountType, setNewAccountType] = useState(account.account_type)
  const [newBalance, setNewBalance] = useState(account.balance)

  function handleUpdate() {
    updateAccount(account.id, {bank_name: newBank, account_type: newAccountType, balance: Number(newBalance)}).then(() => {
      onUpdated()
    }).catch(err => console.error(err))
  }
  return (
  <div className = "modal-overlay">
    <div className = "modal-content">
      <h1 className = "absolute top-4 left-4 text-gray-300 text-xl font-semibold">Edit Bank Account</h1>
      <button className = "absolute top-4 right-4 text-white font-semibold" onClick = {onClose}>Close</button>

      <div className = "flex gap-4">
        <div className = "w-full">
          <input className = "modal-input" placeholder = "Enter Bank Name" value = {newBank} onChange = {(e) => setNewBank(e.target.value)}></input>
        </div>
      </div>

      <div className = "flex gap-4">
        <div className = "w-full">
          <h2 className = "text-white font-semibold">Select Account Type</h2>
          <select className = "modal-input" value = {newAccountType} onChange = {(e) => setNewAccountType(e.target.value)}>
          <option value = "checking">Checking</option> 
          <option value = "savings">Saving</option> 
          <option value = "credit">Credit</option> 
          </select>
        </div>
        <div className = "w-full">
          <h2 className = "text-white font-semibold">Enter Balance</h2>
          <input className = "modal-input" value = {newBalance} onChange = {(e) => setNewBalance(e.target.value)}></input> 
        </div>
      </div>

      <button className = "text-white font-semibold" onClick = {handleUpdate}>Save Changes</button>
    </div>
  </div>
  )
}
export default EditAccountModal