import {useState, useEffect} from "react"
import {createTransaction} from "../api/api"

function CreateTransactionModal({accounts, categories, onCreated, onClose}) {
  const [account_id, setAccountID] = useState(accounts[0].id) 
  const [category_id, setCategoryID] = useState(categories[0].id)
  const [amount, setAmount] = useState(0)
  const [transaction_type, setTransactionType] = useState("income")
  const [description, setDescription] = useState("")
  const [date, setDate] = useState("")

  function handleCreate() {
    createTransaction({account_id: Number(account_id), category_id: Number(category_id), amount: Number(amount), transaction_type: transaction_type, description: description, date: date}).then(() => {
      onCreated()
    }).catch(err => console.error(err))
  }

  return (
    <div className = "modal-overlay">
      <div className = "modal-content">
        <h1 className = "absolute top-4 left-4 text-gray-300 text-xl font-semibold">Create New Transaction</h1>
        <button className = "absolute top-4 right-4 text-white font-semibold" onClick = {onClose}>Close</button>

        <div className = "flex gap-4">
          <div className = "w-full">
            <h2 className = "text-white font-semibold">Select Account</h2>
            <select className = "modal-input" value = {account_id} onChange = {(e) => setAccountID(e.target.value)}>
              {accounts.map(account =>
                <option key = {account.id} value = {account.id}>{account.bank_name}</option>
              )}
            </select> 
          </div>
          <div className = "w-full">
            <h2 className = "text-white font-semibold">Select Category</h2>
            <select className = "modal-input" value = {category_id} onChange = {(e) => setCategoryID(e.target.value)}>
              {categories.map(category =>
                <option key = {category.id} value = {category.id}>{category.name}</option>
              )}
            </select>
          </div>
        </div>

        <div className = "flex gap-4">  
          <div className = "w-full">
            <h2 className = "text-white font-semibold">Enter Amount</h2>
            <input className = "modal-input" placeholder = "Enter Amount" value = {amount} onChange = {(e) => setAmount(e.target.value)}></input>
          </div>
          <div className = "w-full">
            <h2 className = "text-white font-semibold">Select Type</h2>
            <select className = "modal-input" value = {transaction_type} onChange = {(e) => setTransactionType(e.target.value)}>
              <option value = "income">Income</option>
              <option value = "expense">Expense</option>
            </select>
          </div>
        </div>

        <div className = "flex gap-4">   
          <div className = "w-full">   
            <h2 className = "text-white font-semibold">Description</h2>
            <input className = "modal-input" value = {description} onChange = {(e) => setDescription(e.target.value)}></input>
          </div>
          <div className = "w-full">
            <h2 className = "text-white font-semibold">Date of Transaction</h2>
            <input className = "modal-input" type = "date" value = {date} onChange = {(e) => setDate(e.target.value)}></input> 
          </div>
        </div>

        <button className = "text-white font-semibold" onClick = {handleCreate}>Create</button>
        
      </div>
    </div> 
  )
}
export default CreateTransactionModal


