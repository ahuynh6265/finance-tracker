import {useState} from "react"
import {updateTransaction} from "../api/api"

function EditTransactionModal({transaction, accounts, categories, onUpdated, onClose}) {
  const [newAccountID, setNewAccountID] = useState(transaction.account_id)
  const [newCategoryID, setNewCategoryID] = useState(transaction.category_id)
  const [newAmount, setNewAmount] = useState(transaction.amount)
  const [newTransactionType, setNewTransactionType] = useState(transaction.transaction_type)
  const [newDescription, setNewDescription] = useState(transaction.description)
  const [newDate, setNewDate] = useState(transaction.date)

  function handleUpdate() {
    updateTransaction(transaction.id, {account_id: Number(newAccountID), category_id: Number(newCategoryID), amount: Number(newAmount), transaction_type: newTransactionType, description: newDescription, date: newDate}).then(() => {
      onUpdated()
    }).catch(err => console.error(err))
  }

  return (
    <div className = "modal-overlay">
      <div className = "modal-content">
        <h1 className = "absolute top-4 left-4 text-gray-300 text-xl font-semibold">Edit Transaction</h1>
        <button className = "absolute top-4 right-4 text-white font-semibold" onClick = {onClose}>Close</button>

        <div className = "flex gap-4">
          <div className = "w-full">
            <h2 className = "text-white font-semibold">Select Account</h2>
            <select className = "modal-input" value = {newAccountID} onChange = {(e) => setNewAccountID(e.target.value)}>
              {accounts.map(account =>
                <option key = {account.id} value = {account.id}>{account.bank_name}</option>
              )}
            </select> 
          </div>
          <div className = "w-full">
            <h2 className = "text-white font-semibold">Select Category</h2>
            <select className = "modal-input" value = {newCategoryID} onChange = {(e) => setNewCategoryID(e.target.value)}>
              {categories.map(category =>
                <option key = {category.id} value = {category.id}>{category.name}</option>
              )}
            </select>
          </div>
        </div>

        <div className = "flex gap-4">  
          <div className = "w-full">
            <h2 className = "text-white font-semibold">Enter Amount</h2>
            <input className = "modal-input" placeholder = "Enter Amount" value = {newAmount} onChange = {(e) => setNewAmount(e.target.value)}></input>
          </div>
          <div className = "w-full">
            <h2 className = "text-white font-semibold">Select Type</h2>
            <select className = "modal-input" value = {newTransactionType} onChange = {(e) => setNewTransactionType(e.target.value)}>
              <option value = "income">Income</option>
              <option value = "expense">Expense</option>
            </select>
          </div>
        </div>

        <div className = "flex gap-4">   
          <div className = "w-full">   
            <h2 className = "text-white font-semibold">Description</h2>
            <input className = "modal-input" value = {newDescription} onChange = {(e) => setNewDescription(e.target.value)}></input>
          </div>
          <div className = "w-full">
            <h2 className = "text-white font-semibold">Date of Transaction</h2>
            <input className = "modal-input" type = "date" value = {newDate} onChange = {(e) => setNewDate(e.target.value)}></input> 
          </div>
        </div>

        <button className = "text-white font-semibold" onClick = {handleUpdate}>Save</button>
      </div>
    </div>
  )
}
export default EditTransactionModal