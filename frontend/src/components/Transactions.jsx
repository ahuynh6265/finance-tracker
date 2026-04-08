import {useState, useEffect} from "react"
import {getTransactions, deleteTransaction, getAccounts, getCategories, deleteCategoryTransactions, refreshData} from "../api/api"
import TransactionModal from "./TransactionModal"

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

  //sorting 
  const [sort, setSort] = useState("date")
  const [dir, setDir] = useState("desc")

  //filter
  const [filterMonth, setFilterMonth] = useState("")
  const [filterCategory, setFilterCategory] = useState("")

  //pages 
  const [currentPage, setCurrentPage] = useState(1)
  const [entriesPerPage, setEntriesPerPage] = useState(10)
 
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

  function handleSort(column) {
    if (sort === column) {
      setDir((prevState) => (prevState === "desc" ? "asc" : "desc"))
    }
    else {
      setSort(column)
      if (column === "date") {setDir("desc")}
      else {setDir("asc")}
    }
  }

  //clear transaction from select category
  function handleClearCategoryTransactions(category_id) {
    setError("")
    deleteCategoryTransactions(category_id).then(() => {
      refreshData(getTransactions, setTransactions).then(() => refreshData(getAccounts, setAccounts)).then(() => refreshData(getCategories, setCategories))
    }).catch(err => {
      if (err.response) {
        setError(err.response.data.detail)
      }
      else {
        setError("Something went wrong.")
      }
    })
  }

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
  else {
  let copyTransactions = [...transactions]

  if (filterMonth !== ""){
    copyTransactions = copyTransactions.filter(t => t.date.split("-")[1] === filterMonth)
  }
  if (filterCategory !== ""){
    copyTransactions = copyTransactions.filter(t => t.category_id === Number(filterCategory))
  }
  if (sort === "date") {
    if (dir === "desc") {copyTransactions.sort((a, b) => b.date.localeCompare(a.date))}
    else {copyTransactions.sort((a, b) => a.date.localeCompare(b.date))}
  }
  else if (sort === "category_id"){
    copyTransactions.sort((a, b) => {
      const nameA = categories.find(c => c.id === a.category_id)?.name || ""
      const nameB = categories.find(c => c.id === b.category_id)?.name || ""
      if (dir === "desc") {return nameB.localeCompare(nameA)}
      else {return nameA.localeCompare(nameB)}
    })
  }
  else if (sort === "account_id"){
    copyTransactions.sort((a, b) => {
      const nameA = accounts.find(acc => acc.id === a.account_id)?.bank_name || ""
      const nameB = accounts.find(acc => acc.id === b.account_id)?.bank_name || ""
      if (dir === "desc") {return nameB.localeCompare(nameA)}
      else {return nameA.localeCompare(nameB)}
    })
  }
  else if (sort === "amount"){
    copyTransactions.sort((a, b) => {
      if (dir === "desc") {return Number(b.amount) - Number(a.amount)}
      else {return Number(a.amount) - Number(b.amount)}
    })
  }
  else if (sort === "description"){
    copyTransactions.sort((a, b) => {
      if (dir === "desc") {return b.description.localeCompare(a.description)}
      else {return a.description.localeCompare(b.description)}
    })
  }
  else {
    copyTransactions.sort((a, b) => {
      if (dir === "desc") {return b.transaction_type.localeCompare(a.transaction_type)}
      else {return a.transaction_type.localeCompare(b.transaction_type)}
    })
  }

  function getPageNumbers() {
    if (entriesPerPage === "") {return []}
    else {
      const totalPages = Math.ceil(copyTransactions.length / entriesPerPage)
      let pages = []
      if (totalPages > 5) {
        if (currentPage <= 3) {
          pages = [1, 2, 3, 4, 5, "...", totalPages]
        }
        else if (currentPage >= totalPages - 2) {
          pages = [1, "...", totalPages - 4, totalPages - 3, totalPages - 2, totalPages - 1, totalPages]
        }
        else {
          pages = [1, "...", currentPage - 1, currentPage, currentPage + 1, "...", totalPages]
        }
        return pages
      }
      else {
        pages = Array.from({length: totalPages}, (_, i) => i + 1)
        return pages
      }
    }
  }

  const start = (currentPage - 1) * entriesPerPage 
  const end = currentPage * entriesPerPage
  const paginatedTransaction = copyTransactions.slice(start, end)
  const displayTransactions = entriesPerPage === "" ? copyTransactions : paginatedTransaction

  
  return (
    <div>
      {guardTransactions()}
      <button className = "text-white font-semibold" disabled = {accounts.length === 0 || categories.length === 0} onClick = {(e) => setShowCreate(true)}>Create Transaction</button>
      <select value = {filterMonth} onChange = {(e) => setFilterMonth(e.target.value)}>
        <option value = "">Show All Months</option>
        <option value = "01">January</option>
        <option value = "02">February</option>
        <option value = "03">March</option>
        <option value = "04">April</option>
        <option value = "05">May</option>
        <option value = "06">June</option>
        <option value = "07">July</option>
        <option value = "08">August</option>
        <option value = "09">September</option>
        <option value = "10">October</option>
        <option value = "11">November</option>
        <option value = "12">December</option>
      </select>
      <select value = {filterCategory} onChange = {(e) => setFilterCategory(e.target.value)}>
        <option value = "">Show All Categories</option>
        {categories.map(category => 
          <option key = {category.id} value = {category.id}>{category.name}</option>
        )}
      </select>

      {showCreate ? (
      <TransactionModal
        transaction = {null}
        accounts = {accounts}
        categories = {categories}
        onSuccess = {() => {
          refreshData(getTransactions, setTransactions)
          setShowCreate(false)
        }}
        onClose = {() => setShowCreate(false)}
      />
      ) : null}

      {current_id ? (
        <TransactionModal
        transaction = {transactions.find (t => t.id  === current_id)}
        accounts = {accounts}
        categories = {categories}
        onSuccess = {() => {
          refreshData(getTransactions, setTransactions)
          setID(null)
        }}
        onClose = {() => setID(null)}
        />
      ): null}
        <div className = "transactions-table border border-gray-600 rounded-xl">
        <table className = "w-full table-fixed"> 
          <thead>
            <tr>
              <th className = " p-3" onClick = {() => handleSort("account_id")}>Account</th>
              <th className = " p-3" onClick = {() => handleSort("category_id")}>Category</th>
              <th className = " p-3" onClick = {() => handleSort("amount")}>Amount</th>
              <th className = " p-3" onClick = {() => handleSort("transaction_type")}>Type</th>
              <th className = "p-3" onClick = {() => handleSort("description")}>Description</th>
              <th className = " p-3" onClick = {() => handleSort("date")}>Date</th>
              <th>Actions</th>
            </tr>
          </thead>
        <tbody> 
        {displayTransactions.map(transaction =>
          <tr key = {transaction.id}>
              <td>{accounts.find(a => a.id === transaction.account_id)?.bank_name || "Unknown"}</td>
              <td>{categories.find(c => c.id === transaction.category_id)?.name || "Unknown"}</td>
              <td>{transaction.amount}</td>
              <td>{transaction.transaction_type}</td>
              <td className = "break-words">{transaction.description}</td>
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
      <select value = {entriesPerPage} onChange = {(e) => {setEntriesPerPage(e.target.value); setCurrentPage(1)}}>
        <option value = "1">1</option>
        <option value = "10">10</option>
        <option value = "25">25</option>
        <option value = "">All</option>
      </select>
      {getPageNumbers().map((page, index) => 
        page === "..." 
        ? <span key = {index}>{page}</span> 
        : <button className = "text-white" key = {index} onClick={() => setCurrentPage(page)}>{page}</button>
      )}
      <div className = "flex justify-end">
        <select value = {category_id} onChange = {(e) => setCategoryID(e.target.value)}>
          <option value = "">Select Clear</option>
          {categories.map(category => 
          <option key = {category.id} value = {category.id}>{category.name}</option>
          )}
        </select>
        <button disabled = {category_id === ""} onClick = {() => handleClearCategoryTransactions(category_id)}>Clear</button>
      </div>
      <div className = "text-red-400">{error}</div>

    </div>
  )
  }
}
export default Transactions