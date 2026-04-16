import {useState, useEffect} from "react"
import {Link} from "react-router-dom"
import {getAccounts, getCategories, deleteAccount, refreshData, handleAPIError, getSummary, getAccountSummary, getAccountTransactions} from "../api/api"
import AccountModal from "./AccountModal"
import AccountTransferModal from "./AccountTransferModal"

function Accounts() {
  const [summary, setSummary] = useState(null)
  const [categories, setCategories] = useState(null)
  const [accounts, setAccounts] = useState(null)
  const [accountSummary, setAccountSummary] = useState(null)
  const [accountTransactions, setAccountTransactions] = useState(null)
  const [selectedAccountID, setSelectedAccountID] = useState(null)
  const [current_id, setID] = useState(null)
  const [showCreate, setShowCreate] = useState(false)
  const [showTransfer, setShowTransfer] = useState(false)
  const [error, setError] = useState("")

  useEffect (() => {
    refreshData(getAccounts, setAccounts).then((accounts) => setSelectedAccountID(accounts[0]?.id || ""))
    refreshData(getCategories, setCategories)
    refreshData(getSummary, setSummary)
  }, [])

  useEffect(() => {
    if (!selectedAccountID) return 
    getAccountSummary(selectedAccountID).then(response => {
      setAccountSummary(response.data)
    })
    getAccountTransactions(selectedAccountID).then(response => {
      setAccountTransactions(response.data)
    })
  }, [selectedAccountID])

  function handleDelete(account_id) {
    setError("")
    deleteAccount(account_id).then(() => refreshData(getAccounts, setAccounts)).catch(err => {setError(handleAPIError(err))})
  }

  if (!accounts || !summary) return <div>Loading...</div>

  else {
    if (accounts.length === 0) {
      return (<div>
        <div className ="text-gray-800">No Accounts yet</div>
        <button className = "text-gray-800" onClick = {(e) => setShowCreate(true)}>Add Account</button>
        {showCreate ? (
          <AccountModal
          account = {null}
          onSuccess = {() => {
            refreshData(getAccounts, setAccounts)
            setShowCreate(false)
          }}
          onClose = {() => setShowCreate(false)}
          />
        ): null}
      </div>)
    }
    else {
      let copyAccountTransactions = accountTransactions

     
      const currentMonth = new Date().getMonth() + 1;
      const currentYear = new Date().getFullYear();

      if (copyAccountTransactions !== null){
        copyAccountTransactions = copyAccountTransactions.filter(a => Number(a.date.split("-")[1]) === Number(currentMonth) && Number(a.date.split("-")[0]) === Number(currentYear))

        copyAccountTransactions = copyAccountTransactions.sort((a,b) => b.date.localeCompare(a.date))
      }
      
      return (
        <div>
          <select value = {selectedAccountID} onChange = {(e) => setSelectedAccountID(e.target.value)}>
            <option value = "">All Accounts</option>
            {accounts.map(account => 
              <option key = {account.id} value = {account.id}>{account.bank_name} - <span className ="capitalize">{account.account_type}</span></option>
            )}
          </select>
          {(selectedAccountID && accountSummary != null) ? (
            <>
              <div className = "flex gap-4 mt-6 ">
                <div className = "card">
                  <div className = "text-gray-900 text-sm">Expenses This Month</div>
                  <div>${accountSummary.expenses}</div>
                </div>

                <div className = "card">
                  <div className = "text-gray-900 text-sm">Net Balance This Month</div>
                  <div>${accountSummary.net_balance}</div>
                </div>
              </div>

              <div className = "flex gap-4 mt-6 h-64">
                <div className = "card">
                  <div>Account Chart</div>
                </div>
              </div>

              <div className = "flex gap-4 mt-6 h-64">
                <div className = "card relative flex flex-col">
                  <div className = "p-4">Account Transactions This Month</div>
                  <Link className = "absolute top-4 right-4" to = "/transactions">See All Transactions</Link>
                  {copyAccountTransactions && copyAccountTransactions.length > 0 && categories ? (
                    <div className ="transactions-table overflow-y-auto "> 
                    <table className = "w-full table-fixed">
                      <thead>
                        <tr>
                          <th>Category</th>
                          <th>Amount</th>
                          <th>Type</th>
                          <th>Description</th>
                          <th>Date</th>
                        </tr>
                      </thead>
                      <tbody>
                        {copyAccountTransactions.map(transaction =>
                            <tr key = {transaction.id}>
                              <td>{categories.find(c => c.id === transaction.category_id)?.name || "Unknown"}</td>
                              <td>${transaction.amount}</td>
                              <td>{transaction.transaction_type}</td>
                              <td>{transaction.description}</td>
                              <td>{transaction.date}</td>
                            </tr>
                          )
                        }
                      </tbody>
                    </table>
                  </div>
                  ) : <div className = "p-4">No transactions this month</div>}
                </div>
              </div>
            </>
          ) : (
            <div>
              <button className = "text-gray-800" onClick = {(e) => setShowCreate(true)}>Add Account</button>
              <button className = "text-gray-800" onClick = {(e) => setShowTransfer(true)}>Transfer Money</button>
              <div className = "text-red-600">{error}</div>
              {showCreate ? (
                <AccountModal
                account = {null}
                onSuccess = {() => {
                  refreshData(getAccounts, setAccounts)
                  setShowCreate(false)
                }}
                onClose = {() => setShowCreate(false)}
                />
              ): null}

              {current_id ? (
                <AccountModal
                account = {accounts.find (a => a.id === current_id)}
                onSuccess = {() => {
                  refreshData(getAccounts, setAccounts)
                  setID(null)
                }}
                onClose = {() => setID(null)}
                />
              ): null}

              {showTransfer ? (
                <AccountTransferModal 
                accounts = {accounts}
                onSuccess = {() => {
                  refreshData(getAccounts, setAccounts)
                  setShowTransfer(null)
                }}
                onClose = {() => setShowTransfer(null)}
                />
              ): null}

              <div className = "flex gap-4 mt-6">
                <div className = "card w-[55%]">
                  <h2 className = "text-gray-900 font-semibold m-6">Connected Cards</h2>
                  <div className = "h-[300px] overflow-y-auto pb-2">
                    {accounts.map(account =>
                      <div className= "card mx-6 mb-6 p-2" key = {account.id}>
                        <div className = "flex justify-between">

                          <div>
                            <div className = "text-gray-800 font-semibold">{account.bank_name}</div>
                            <div className = "text-gray-500 text-sm">{account.account_type}</div>
                            <div className = "text-gray-800 text-xl">{account.balance}</div>
                          </div>

                          <div className = "flex justify-center">
                            <button className = "mr-2" onClick = {() => handleDelete(account.id)}>Delete</button>
                            <button onClick = {() => {setID(account.id)}}>Edit</button>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              
                <div className = "flex flex-col w-[45%] gap-4">
                  <div className = "flex gap-4 h-[50%]">
                    <div className = "card p-4">
                      <div className = "text-gray-900 text-sm">Total Balance</div>
                      <div className = "text-gray-800 text-2xl">${summary["net balance"]}</div>
                    </div>
                    <div className = "card p-4">
                      <div className = "text-gray-900 text-sm">Available Balance</div>
                      <div className = "text-gray-800 text-2xl">${summary.accounts_only}</div>
                    </div>
                  </div>
                  <div className = "flex gap-4 h-[50%]">
                    <div className = "card p-4">
                      <div className = "text-gray-900 text-sm">Allocated to Goals</div>
                      <div className = "text-gray-800 text-2xl">${summary.goals_only}</div>
                    </div>
                    <div className = "card p-4">
                      <div className = "text-gray-900 text-sm">Active Accounts</div>
                      <div className = "text-gray-800 text-2xl">{accounts.length}</div>
                    </div>
                  </div>
                </div>
              </div> 

              <div className = "flex gap-4 mt-4 justify-end">
                <div className = "flex flex-col w-[55%] h-96 rounded-xl">
                    <div className = "card">
                      <h2 className = "text-gray-900 font-semibold m-6">Balance Overview</h2>
                      <div></div>
                    </div>
                </div>
              </div>
            </div>
          )}

        </div>
      )
    }
  }
}

export default Accounts

