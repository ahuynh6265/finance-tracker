import {useState, useEffect} from "react"
import {getTransactions, createTransaction, deleteTransaction, updateTransaction, getAccounts, getCategories, deleteCategory, createCategory, updateCategory} from "../api/api"

function Transactions(){
  //transaction variables
  const [transactions, setTransactions] = useState(null)
  const [accounts, setAccounts] = useState(null)
  const [categories, setCategories] = useState(null)
  const [account_id, setAccountID] = useState("")
  const [category_id, setCategoryID] = useState("")
  const [amount, setAmount] = useState(0)
  const [transaction_type, setTransactionType] = useState("income")
  const [description, setDescription] = useState("")
  const [date, setDate] = useState("")

  //transaction updates
  const [current_id, setID] = useState(null)
  const [newAccountID, setNewAccountID] = useState("")
  const [newCategoryID, setNewCategoryID] = useState("")
  const [newAmount, setNewAmount] = useState(0)
  const [newTransactionType, setNewTransactionType] = useState("income")
  const [newDescription, setNewDescription] = useState("")
  const [newDate, setNewDate] = useState("")
  
  //modal 
  const [showCreate, setShowCreate] = useState(false)
  const [showCategories, setShowCategories] = useState(false)
  const [showCreateCategories, setShowCreateCategories] = useState(false)

  //category 
  const [name, setName] = useState("")
  const [newName, setNewName] = useState("")
  const [editCategoryID, setEditCategoryID] = useState("")

  useEffect (() => {
    getTransactions().then(response => {
      setTransactions(response.data)
    }).catch(err => console.error(err))
    getAccounts().then(response => {
      setAccounts(response.data)
      if (response.data.length > 0){
        setAccountID(response.data[0].id)
      }
    }).catch(err => console.error(err))
    getCategories().then(response => {
      setCategories(response.data)
      if (response.data.length > 0){
        setCategoryID(response.data[0].id)
      }
    }).catch(err => console.error(err))
  }, [])

  function handleCreate() {
    createTransaction({account_id: Number(account_id), category_id: Number(category_id), amount: Number(amount), transaction_type: transaction_type, description: description, date: date}).then(() => getTransactions().then(response => {
      setTransactions(response.data)
      setAccountID(Number(accounts[0].id))
      setCategoryID(Number(categories[0].id))
      setAmount(Number(0))
      setTransactionType("income")
      setDescription("")
      setDate("")
      setShowCreate(false)
    }).catch(err => console.error(err)))
  }

  function handleDelete(transaction_id) {
    deleteTransaction(transaction_id).then(() => getTransactions().then(response => {
      setTransactions(response.data)
    }).catch(err => console.error(err)))
  }

  function handleUpdate(transaction_id) {
    updateTransaction(transaction_id, {account_id: Number(newAccountID), category_id: Number(newCategoryID), amount: Number(newAmount), transaction_type: newTransactionType, description: newDescription, date: newDate}).then(() => getTransactions().then(response => {
      setTransactions(response.data)
      setID(null)
      setNewAccountID(Number(accounts[0].id))
      setNewCategoryID(Number(categories[0].id))
      setNewAmount(Number(0))
      setNewTransactionType("income")
      setNewDescription("")
      setNewDate("")
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

  function handleCreateCategory() {
    createCategory({name: name}).then(() => getCategories().then(response => {
      setCategories(response.data)
      setName("")
      setShowCreateCategories(false)
    }).catch(err => console.error(err)))
  }

  function handleUpdateCategory(category_id) {
    updateCategory(category_id, {name: newName}).then(() => getCategories().then(response => {
      setCategories(response.data)
      setEditCategoryID("")
      setNewName("")
    }).catch(err => console.error(err)))
  }

  if (!transactions || !accounts || !categories) return <div>Loading...</div>
  else return (
    <div>
    <button onClick = {(e) => setShowCreate(true)}>Create Transaction</button>
    <button onClick = {(e) => setShowCategories(true)}>Manage Categories</button> 
    {showCreate ? (
      <div className = "modal-overlay">
        <div className = "modal-content">
          <h1 className = "absolute top-4 left-4 text-gray-300 text-xl font-semibold">Create New Transaction</h1>
          <button className = "absolute top-4 right-4 text-white font-semibold" onClick = {(e) => setShowCreate(false)}>Close</button>

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
    ) : null}

    {showCategories ? (
      <div className = "modal-overlay">
        <div className = "modal-content">
          <h1 className = "absolute top-4 left-4 text-gray-300 text-xl font-semibold">Manage Categories</h1>
          <button className = "absolute top-4 right-4 text-white font-semibold" onClick = {(e) => {setShowCategories(false); setEditCategoryID("")}}>Close</button>
          <table>
            <tbody>
              {categories.map(category =>
                <tr key = {category.id}> 
                  {(editCategoryID === category.id) ? (
                    <>
                      <td><input value = {newName} onChange = {(e) => setNewName(e.target.value)}></input></td>
                      <td><button onClick = {(e) =>handleUpdateCategory(category.id)}>Save Category</button></td>
                    </>
                  ): (
                    <>
                    <td>{category.name}</td>
                        <td>
                          <button className = "mr-2" onClick = {() =>handleDeleteCategory(category.id)}>Delete</button>
                          <button onClick = {() => {setEditCategoryID(category.id); setNewName(category.name)}}>Edit</button>
                        </td>
                      </>
                  )}
                </tr>
              )}
            </tbody>
          </table>
          <button onClick = {(e) => setShowCreateCategories(true)}>Create</button> 
          {(showCreateCategories) ? (
            <div className = "-mt-4">
              <input className = "w-full" placeholder = "Enter Category Name" value = {name} onChange = {(e) => setName(e.target.value)}></input>
              <div className = "flex justify-around p-6">
                <button className = "text-gray-300 text-l font-semibold" onClick = {handleCreateCategory}>Save Category</button>
                <button className = "text-gray-300 text-l font-semibold" onClick = {(e) => setShowCreateCategories(false)}>Discard</button>
              </div>
            </div>
          ): null}  
        </div>
    </div> 
    ): null}
    {current_id ? (
      <div className = "modal-overlay">
        <div className = "modal-content">
          <h1 className = "absolute top-4 left-4 text-gray-300 text-xl font-semibold">Edit Transaction</h1>
          <button className = "absolute top-4 right-4 text-white font-semibold" onClick = {(e) => setID(null)}>Close</button>

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

          <button className = "text-white font-semibold" onClick = {(e) => handleUpdate(current_id)}>Save</button>
        </div>
      </div>
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
              <button onClick = {() => {setID(transaction.id); setNewAccountID(transaction.account_id); setNewCategoryID(transaction.category_id); setNewAmount(transaction.amount); setNewTransactionType(transaction.transaction_type); setNewDescription(transaction.description); setNewDate(transaction.date)}}>Edit</button>
            </td>
         </tr>
      )}
      </tbody>
    </table>
    </div>
  )
}

export default Transactions