import {useState, useEffect} from "react"
import {getTransactions, deleteTransaction, getAccounts, getCategories, deleteCategoryTransactions, refreshData} from "../api/api"
import CreateTransactionModal from "./CreateTransactionModal"
import EditTransactionModal from "./EditTransactionModal"

function Transactions(){
  //transaction variables
  const [transactions, setTransactions] = useState(null)
  const [accounts, setAccounts] = useState(null)
  const [categories, setCategories] = useState(null)
  const [category_id, setCategoryID] = useState("")

  //transaction updates
  const [current_id, setID] = useState(null)
  
  //modal 
  const [showCreate, setShowCreate] = useState(false)
  const [error, setError] = useState("")

  useEffect (() => {
    refreshData(getTransactions, setTransactions)
    refreshData(getAccounts, setAccounts)
    refreshData(getCategories, setCategories)
  }, [])

  function handleDelete(transaction_id) {
    setError("")
    deleteTransaction(transaction_id).then(() => refreshData(getTransactions, setTransactions)).catch(err => {
      if (err.response) {
        setError(err.response.data.detail)
      }
      else {
        setError("Something went wrong.")
      }
    })
  }

  //clear transaction from select category
  /*
  function handleClearCategoryTransactions(category_id) {
    setError("")
    deleteCategoryTransactions(category_id).then(() => {
      refreshData(getTransactions, setTransactions).then(() => refreshData(getCategories, setCategories))
    })
  }*/

  function guardTransactions() {
    return(
    <div>
      {(accounts.length === 0 && categories.length === 0) ? (
        <p className = "text-white font-semibold">Add an Account or Category before creating a transaction</p>
      ): null}
      {(accounts.length === 0 && categories.length > 0) ? (
        <p className = "text-white font-semibold">Add an Account before creating a transaction</p>
      ): null}
      {(categories.length === 0 && accounts.length > 0) ? (
        <p className = "text-white font-semibold">Add a Category before creating a transaction</p>
      ): null}
    </div>
    )
  }

  if (!transactions || !accounts || !categories) return <div>Loading...</div>
  else return (
    <div>
    {guardTransactions()}
    <button className = "text-white font-semibold" disabled = {accounts.length === 0 || categories.length === 0} onClick = {(e) => setShowCreate(true)}>Create Transaction</button>

    {showCreate ? (
    <CreateTransactionModal
      accounts = {accounts}
      categories = {categories}
      onCreated = {() => {
        refreshData(getTransactions, setTransactions)
        setShowCreate(false)
      }}
      onClose = {() => setShowCreate(false)}
    />
    ) : null}

    {current_id ? (
      <EditTransactionModal
      transaction = {transactions.find (t => t.id  === current_id)}
      accounts = {accounts}
      categories = {categories}
      onUpdated = {() => {
        refreshData(getTransactions, setTransactions)
        setID(null)
      }}
      onClose = {() => setID(null)}
      />
    ): null}

      <table className = "transactions-table"> 
        <thead>
          <tr>
            <th>Account</th>
            <th>Category</th>
            <th>Amount</th>
            <th>Type</th>
            <th>Description</th>
            <th>Date</th>
            <th>Actions</th>
          </tr>
        </thead>
      <tbody> 
      {transactions.map(transaction =>
        <tr key = {transaction.id}>
            <td>{accounts.find(a => a.id === transaction.account_id)?.bank_name || "Unknown"}</td>
            <td>{categories.find(c => c.id === transaction.category_id)?.name || "Unknown"}</td>
            <td>{transaction.amount}</td>
            <td>{transaction.transaction_type}</td>
            <td>{transaction.description}</td>
            <td>{transaction.date}</td>
            <td>
              <button className ="mr-2" onClick = {() => handleDelete(transaction.id)}>Delete</button>
              <button onClick = {() => {setID(transaction.id)}}>Edit</button>
            </td>
         </tr>
      )}
      </tbody>
    </table>
    <div className = "text-red-400">{error}</div>
    </div>
  )
}

export default Transactions