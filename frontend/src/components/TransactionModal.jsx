import {useState} from "react"
import {createTransaction, updateTransaction} from "../api/api"

function TransactionModal({transaction, accounts, categories, onSuccess, onClose}) {
  const [error, setError] = useState("")
  const [account_id, setAccountID] = useState(transaction ? transaction.account_id : accounts[0].id) 
  const [category_id, setCategoryID] = useState(transaction ? transaction.category_id : categories[0].id)
  const [amount, setAmount] = useState(transaction ? transaction.amount : 0)
  const [transaction_type, setTransactionType] = useState(transaction ? transaction.transaction_type : "income")
  const [description, setDescription] = useState(transaction ? transaction.description : "")
  const [date, setDate] = useState(transaction ? transaction.date : "")

  function handleSubmit() {
    setError("")
     //need to check if amount is anything but numerical or else pydantic will reject with own message
    if (isNaN(Number(amount))){ 
      setError("Please enter a numerical value.")
    } 
    else if (date === ""){
      setError("Please select a date.")
    }
    else if (transaction === null) {
      createTransaction({account_id: Number(account_id), category_id: Number(category_id), amount: Number(amount), transaction_type: transaction_type, description: description, date: date}).then(() => {
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
      updateTransaction(transaction.id, {account_id: Number(account_id), category_id: Number(category_id), amount: Number(amount), transaction_type: transaction_type, description: description, date: date}).then(() => {
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
        {transaction ? (<h1 className = "absolute top-4 left-4 text-gray-300 text-xl font-semibold">Edit Transaction</h1>) : (<h1 className = "absolute top-4 left-4 text-gray-300 text-xl font-semibold">Create New Transaction</h1>)}
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
                (category.name !== "Transfer") ? (
                  <option key = {category.id} value = {category.id}>{category.name}</option>
                ) : (null)
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

        {transaction ? ( <button className = "text-white font-semibold" onClick = {handleSubmit}>Save</button>) : ( <button className = "text-white font-semibold" onClick = {handleSubmit}>Create</button>)}
        <div className = "text-red-400">{error}</div>
      </div>
    </div>
  )
}
export default TransactionModal 