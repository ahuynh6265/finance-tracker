import {useState, useEffect} from "react"
import {getTransactions, deleteTransaction, getAccounts, getCategories, deleteCategory} from "../api/api"
import CreateTransactionModal from "./CreateTransactionModal"
import EditTransactionModal from "./EditTransactionModal"
import ManageCategoriesModal from "./ManageCategoriesModal"

function Transactions(){
  //transaction variables
  const [transactions, setTransactions] = useState(null)
  const [accounts, setAccounts] = useState(null)
  const [categories, setCategories] = useState(null)

  //transaction updates
  const [current_id, setID] = useState(null)
  
  //modal 
  const [showCreate, setShowCreate] = useState(false)
  const [showCategories, setShowCategories] = useState(false)



  useEffect (() => {
    getTransactions().then(response => {
      setTransactions(response.data)
    }).catch(err => console.error(err))
    getAccounts().then(response => {
      setAccounts(response.data)
    }).catch(err => console.error(err))
    getCategories().then(response => {
      setCategories(response.data)
    }).catch(err => console.error(err))
  }, [])

  function handleDelete(transaction_id) {
    deleteTransaction(transaction_id).then(() => getTransactions().then(response => {
      setTransactions(response.data)
    }).catch(err => console.error(err)))
  }

  function handleDeleteCategory(category_id) {
    //transactions need to refresh before categories, will crash otherwise
    deleteCategory(category_id).then(() => getTransactions().then(response => {
      setTransactions(response.data)
      getCategories().then(response => {
        setCategories(response.data)
      })
    }).catch(err => console.error(err)))
  }


  if (!transactions || !accounts || !categories) return <div>Loading...</div>
  else return (
    <div>
    <button onClick = {(e) => setShowCreate(true)}>Create Transaction</button>
    <button onClick = {(e) => setShowCategories(true)}>Manage Categories</button> 
    {showCreate ? (
    <CreateTransactionModal
      accounts = {accounts}
      categories = {categories}
      onCreated = {() => {
        getTransactions().then(response => setTransactions(response.data))
        setShowCreate(false)
      }}
      onClose = {() => setShowCreate(false)}
    />
    ) : null}

    {showCategories ? (
      <ManageCategoriesModal
      categories = {categories}
      onDeleteCategory = {handleDeleteCategory}
      onCategoryChanged = {() => {
        getCategories().then(response => setCategories(response.data))
      }}
      onClose = {() => setShowCategories(false)}
      />
    ): null}

    {current_id ? (
      <EditTransactionModal
      transaction = {transactions.find (t => t.id  === current_id)}
      accounts = {accounts}
      categories = {categories}
      onUpdated = {() => {
        getTransactions().then(response => setTransactions(response.data))
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
    </div>
  )
}

export default Transactions