import {useState, useEffect} from "react"
import {getTransactions, createTransaction, deleteTransaction, updateTransaction, getAccounts, getCategories} from "../api/api"

function Transactions(){
  const [transactions, setTransactions] = useState(null)
  const [accounts, setAccounts] = useState(null)
  const [categories, setCategories] = useState(null)
  const [account_id, setAccountID] = useState("")
  const [category_id, setCategoryID] = useState("")
  const [amount, setAmount] = useState(0)
  const [transaction_type, setTransactionType] = useState("income")
  const [description, setDescription] = useState("")
  const [date, setDate] = useState("")

  const [current_id, setID] = useState(null)
  const [newAccountID, setNewAccountID] = useState("")
  const [newCategoryID, setNewCategoryID] = useState("")
  const [newAmount, setNewAmount] = useState(0)
  const [newTransactionType, setNewTransactionType] = useState("income")
  const [newDescription, setNewDescription] = useState("")
  const [newDate, setNewDate] = useState("")

  useEffect (() => {
    getTransactions().then(response => {
      setTransactions(response.data)
    })
    getAccounts().then(response => {
      setAccounts(response.data)
      setAccountID(response.data[0].id)
    })
    getCategories().then(response => {
      setCategories(response.data)
      setCategoryID(response.data[0].id)
    })
  }, [])

  function handleCreate() {
    createTransaction({account_id: Number(account_id), category_id: Number(category_id), amount: amount, transaction_type: transaction_type, description: description, date: date}).then(() => getTransactions().then(response => {
      setTransactions(response.data)
      setAccountID(accounts[0].id)
      setCategoryID(categories[0].id)
      setAmount(0)
      setTransactionType("income")
      setDescription("")
      setDate("")
    }))
  }

  function handleDelete(transaction_id) {
    deleteTransaction(transaction_id).then(() => getTransactions().then(response => {
      setTransactions(response.data)
    }))
  }

  function handleUpdate(transaction_id) {
    updateTransaction(transaction_id, {account_id: newAccountID, category_id: newCategoryID, amount: newAmount, transaction_type: newTransactionType, description: newDescription, date: newDate}).then(() => getTransactions().then(response => {
      setTransactions(response.data)
      setID(null)
      setNewAccountID(accounts[0].id)
      setNewCategoryID(categories[0].id)
      setNewAmount(0)
      setNewTransactionType("income")
      setNewDescription("")
      setNewDate("")
    }))
  }

  if (!transactions || !accounts || !categories) return <div>Loading...</div>
  else return (
    <div>
      <select value = {account_id} onChange = {(e) => setAccountID(e.target.value)}>
        {accounts.map(account =>
          <option key = {account.id} value = {account.id}>{account.bank_name}</option>
        )}
      </select> 
      <select value = {category_id} onChange = {(e) => setCategoryID(e.target.value)}>
        {categories.map(category =>
          <option key = {category.id} value = {category.id}>{category.name}</option>
        )}
      </select>
      <input placeholder = "Enter Amount" value = {amount} onChange = {(e) => setAmount(e.target.value)}></input>
      <select value = {transaction_type} onChange = {(e) => setTransactionType(e.target.value)}>
        <option value = "income">Income</option>
        <option value = "expense">Expense</option>
      </select>
      <input placeholder = "Description" value = {description} onChange = {(e) => setDescription(e.target.value)}></input>
      <input type = "date" value = {date} onChange = {(e) => setDate(e.target.value)}></input> 
      <button onClick = {handleCreate}>Create Transaction</button>

      {transactions.map(transaction =>
        <div key = {transaction.id}>
          {(current_id === transaction.id)
          ? (
            <div>
              <select value = {newAccountID} onChange = {(e) => setNewAccountID(e.target.value)}>
                {accounts.map(account =>
                <option key = {account.id} value = {account.id}>{account.bank_name}</option>
                )}
              </select>
              <select value = {newCategoryID} onChange = {(e) => setNewCategoryID(e.target.value)}>
              {categories.map(category =>
                <option key = {category.id} value = {category.id}>{category.name}</option>
              )}
              </select>
              <input value = {newAmount} onChange = {(e) => setNewAmount(e.target.value)}></input>
              <select value = {newTransactionType} onChange = {(e) => setNewTransactionType(e.target.value)}>
                <option value = "income">Income</option>
                <option value = "expense">Expense</option>
              </select>
              <input value = {newDescription} onChange = {(e) => setNewDescription(e.target.value)}></input>
              <input type = "date" value = {newDate} onChange = {(e) => setNewDate(e.target.value)}></input>
              <button onClick = {() => handleUpdate(transaction.id)}>Save Transaction</button>
            </div>
          )
          : (
            <div>
              <div>{accounts.find(a => a.id === transaction.account_id).bank_name} - {categories.find(c => c.id === transaction.category_id).name} - {transaction.amount} - {transaction.transaction_type} - {transaction.description} - {transaction.date}</div>
              <button onClick = {() => handleDelete(transaction.id)}>Delete Transaction</button>
              <button onClick = {() => {setID(transaction.id); setNewAccountID(transaction.account_id); setNewCategoryID(transaction.category_id); setNewAmount(transaction.amount); setNewTransactionType(transaction.transaction_type); setNewDescription(transaction.description); setNewDate(transaction.date)}}> Edit Transaction Info</button>
            </div>
          )
         }</div>
      )}
    </div>
  )
}

export default Transactions