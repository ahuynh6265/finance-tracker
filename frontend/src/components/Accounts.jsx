import {useState, useEffect} from "react"
import {getAccounts, getCategories, deleteAccount, refreshData, handleAPIError, getSummary, getAccountSummary, getAccountTransactions} from "../api/api"
import AccountModal from "./AccountModal"
import AccountTransferModal from "./AccountTransferModal"
import { ResponsiveContainer, LineChart, XAxis, YAxis, CartesianGrid, Tooltip, Line } from 'recharts'
import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import AddIcon from '@mui/icons-material/Add';
import SwapHorizIcon from '@mui/icons-material/SwapHoriz';
import DeleteIcon from '@mui/icons-material/Delete';
import IconButton from '@mui/material/IconButton';
import EditIcon from '@mui/icons-material/Edit';
import {Tooltip as MuiTooltip} from '@mui/material';

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
  const [toggleTimeRange, setToggleTimeRange] = useState("month")

  useEffect (() => {
    refreshData(getAccounts, setAccounts).then((accounts) => setSelectedAccountID(""))
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
    const userConfirm = window.confirm("This action is permanent. Continue?")
    if (userConfirm) {
      deleteAccount(account_id).then(() => refreshData(getAccounts, setAccounts)).then(() => refreshData(getSummary, setSummary)).catch(err => {setError(handleAPIError(err))})
    }
  }

  if (!accounts || !summary) return <div>Loading...</div>

  else {
    if (accounts.length === 0) {
      return (
      <div>
        <div className ="flex flex-col justify-center items-center h-screen">
          <div className ="text-gray-800 text-2xl font-bold mb-4">No Accounts Yet</div>
          <Button variant ="contained" sx={{color: '#D1B0F5', bgcolor: "#E9E8ED", '&:hover': { bgcolor: '#AFAEB0' }}} startIcon ={<AddIcon/>} onClick = {(e) => setShowCreate(true)}>Add Account</Button> 
        </div>
        {showCreate ? (
          <AccountModal
          account = {null}
          onSuccess = {() => {
            refreshData(getAccounts, setAccounts).then(() => refreshData(getSummary, setSummary))
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

      const handleToggle = (event, toggleTimeRange) => {
        setToggleTimeRange(toggleTimeRange)
      }

      let accountChart = []
      let allDates = []
      //chart for per account
      if (accountTransactions !== null) {
        let chartTransactions = accountTransactions
        if (toggleTimeRange === "month"){
          const start = new Date(currentYear, currentMonth - 1, 1)
          const end = new Date(currentYear, currentMonth, 1)
          const cur = new Date(start)
          
          while (cur < end) {
            allDates.push(cur.toISOString().split("T")[0])
            cur.setDate(cur.getDate() + 1)
          }

          chartTransactions = accountTransactions.filter(a => Number(a.date.split("-")[1]) === Number(currentMonth)).sort((a,b) => a.date.localeCompare(b.date))
        }
        else if (toggleTimeRange === "year"){
          for (let i = 1; i <= 12; i++){
            allDates.push(currentYear + "-" + String(i).padStart(2, "0"))
          }
          chartTransactions = accountTransactions
        }
        else {
          const sevenDaysAgo = new Date()
          sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7)
          const sevenDaysAgoString = sevenDaysAgo.toISOString().split("T")[0]
          const end = new Date()

          while (sevenDaysAgo <= end) {
            allDates.push(sevenDaysAgo.toISOString().split("T")[0])
            sevenDaysAgo.setDate(sevenDaysAgo.getDate() + 1)
          }
          chartTransactions = accountTransactions.filter(a => a.date >= sevenDaysAgoString)
        }
        const result = chartTransactions.reduce((accumulator, transaction) => {
          if (transaction.transaction_type === "transfer") return accumulator
          let dateKey = toggleTimeRange === "year" ? transaction.date.split("-").slice(0,2).join("-") : transaction.date
          if (!accumulator[dateKey]) accumulator[dateKey] = 0
          if (transaction.transaction_type === "income") {
            accumulator[dateKey] += Number(transaction.amount)
          }
          else {
            accumulator[dateKey] -= Number(transaction.amount)
          }
          return accumulator
        }, {})
        
        accountChart = allDates.map(date => ({ date: date, net: result[date] || 0 }))
      }

      return (
        <div>
          <div className = "flex flex-row justify-between">
          <div className = "flex flex-row items-center">
            {selectedAccountID === "" ? null : <h1 className = "text-2xl font-semibold text-gray-800 mr-2">Account: </h1>}
              <select className = "select" value = {selectedAccountID} onChange = {(e) => setSelectedAccountID(e.target.value)}>
                <option value = "">All Accounts</option>
                {accounts.map(account => 
                  <option key = {account.id} value = {account.id}>{account.bank_name} - <span className ="capitalize">{account.account_type}</span></option>
                )}
              </select>
            </div>
              <Button startIcon = {<SwapHorizIcon/>} variant ="contained" sx={{color: '#D1B0F5', bgcolor: "#E9E8ED", '&:hover': { bgcolor: '#AFAEB0' }}} onClick = {(e) => setShowTransfer(true)}>Transfer Money</Button>
          </div>
          {(selectedAccountID && accountSummary != null) ? (
            <>
              <div className = "flex gap-4 mt-6 ">
                <div className = "card p-2">
                  <div className = "text-xs font-medium text-gray-500 uppercase tracking-wide">Expenses This Month</div>
                  <div className = "text-2xl font-semibold text-gray-800 mt-1">${Number(accountSummary.expenses).toFixed(2)}</div>
                </div>

                <div className = "card p-2">
                  <div className = "text-xs font-medium text-gray-500 uppercase tracking-wide">Net Balance This Month</div>
                  <div className = "text-2xl font-semibold text-gray-800 mt-1">${Number(accountSummary.net_balance).toFixed(2)}</div>
                </div>
              </div>

              <div className = "flex gap-4 mt-6 mr-6">
                <div className = "card relative flex flex-col">
                  <div className = "font-semibold text-gray-700 p-4">Account Balance</div>
                  <div className = "absolute top-4 right-4">
                    <ToggleButtonGroup
                      value = {toggleTimeRange}
                      exclusive
                      onChange = {handleToggle}
                      >
                      <ToggleButton value="week">
                        Week
                      </ToggleButton>
                      <ToggleButton value="month">
                        Month
                      </ToggleButton>
                      <ToggleButton value="year">
                        Year
                      </ToggleButton>
                    </ToggleButtonGroup>
                  </div>
                  <div className = "mt-5 mr-5">
                    {accountTransactions ? (
                      <ResponsiveContainer width="100%" aspect={1.618} maxHeight={350}>
                      <LineChart
                      data = {accountChart}
                      margin={{
                        top: 5,
                        right: 30,
                        left: 20,
                        bottom: 5,
                      }}
                      >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="date" />
                        <YAxis width={60} />
                        <Tooltip />
                        <Line type="monotone" name="Net Balance" dataKey="net" dot = {false} stroke="#14b8a6"/>
                      </LineChart>
                      </ResponsiveContainer>
                    ) : null}    
                  </div>
                </div>
              </div>

              <div className = "flex gap-4 mt-6 h-64">
                <div className = "card relative flex flex-col">
                  <Stack className = "justify-between" direction = "row">
                    <div className = "font-semibold text-gray-700 p-4">Account Transactions This Month</div>
                    <Button variant = "text" href = "/transactions">See All Transactions</Button>
                  </Stack>
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
                                <td className = {transaction.transaction_type === "transfer" ? "text-gray-800" : (transaction.transaction_type === "income" ? "text-green-600" : "text-red-600")}>${Number(transaction.amount).toFixed(2)}</td>
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
              <div className = "text-red-600">{error}</div>
              {showCreate ? (
                <AccountModal
                account = {null}
                onSuccess = {() => {
                  refreshData(getAccounts, setAccounts).then(() => refreshData(getSummary, setSummary))
                  setShowCreate(false)
                }}
                onClose = {() => setShowCreate(false)}
                />
              ): null}

              {current_id ? (
                <AccountModal
                account = {accounts.find (a => a.id === current_id)}
                onSuccess = {() => {
                  refreshData(getAccounts, setAccounts).then(() => refreshData(getSummary, setSummary))
                  setID(null)
                }}
                onClose = {() => setID(null)}
                />
              ): null}

              {showTransfer ? (
                <AccountTransferModal 
                accounts = {accounts}
                onSuccess = {() => {
                  refreshData(getAccounts, setAccounts).then(() => refreshData(getSummary, setSummary))
                  setShowTransfer(null)
                }}
                onClose = {() => setShowTransfer(null)}
                />
              ): null}

              <div className = "flex gap-4 mt-6">
                <div className = "card w-[55%]">
                  <div className = "flex flex-row relative">  
                    <h2 className = "text-2xl text-gray-900 font-semibold p-4">Connected Cards</h2>
                    <div className = "absolute top-4 right-4">
                      <Button variant ="contained" sx={{color: '#D1B0F5', bgcolor: "#E9E8ED", '&:hover': { bgcolor: '#AFAEB0' }}} startIcon ={<AddIcon/>} onClick = {(e) => setShowCreate(true)}>Add Account</Button>    
                    </div>        
                  </div>
                  <div className = "h-[300px] overflow-y-auto pb-2">
                    {accounts.map(account =>
                      <div className= "card mx-6 mb-6 p-2" key = {account.id}>
                        <div className = "flex justify-between">

                          <div>
                            <div className = "text-gray-800 font-semibold">{account.bank_name}</div>
                            <div className = "text-gray-500 text-sm">{account.account_type}</div>
                            <div className = "text-gray-800 text-xl">${Number(account.balance).toFixed(2)}</div>
                          </div>

                          <div className = "flex justify-center">
                            <MuiTooltip title = "Delete">
                              <IconButton onClick = {() => handleDelete(account.id)}><DeleteIcon/></IconButton>
                            </MuiTooltip>

                            <MuiTooltip title = "Edit">
                              <IconButton onClick = {() => {setID(account.id)}}><EditIcon/></IconButton>
                            </MuiTooltip>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              
                <div className = "flex flex-col w-[45%] gap-4">
                  <div className = "flex gap-4 h-[50%]">
                    <div className = "card p-4">
                      <div className = "text-xs font-medium text-gray-500 uppercase tracking-wide">Total Balance</div>
                      <div className = "text-gray-800 text-2xl font-semibold">${Number(summary["net balance"]).toFixed(2)}</div>
                    </div>
                    <div className = "card p-4">
                      <div className = "text-xs font-medium text-gray-500 uppercase tracking-wide">Available Balance</div>
                      <div className = "text-gray-800 text-2xl font-semibold">${Number(summary.accounts_only).toFixed(2)}</div>
                    </div>
                  </div>
                  <div className = "flex gap-4 h-[50%]">
                    <div className = "card p-4">
                      <div className = "text-xs font-medium text-gray-500 uppercase tracking-wide">Allocated to Goals</div>
                      <div className = "text-gray-800 text-2xl font-semibold">${Number(summary.goals_only).toFixed(2)}</div>
                    </div>
                    <div className = "card p-4">
                      <div className = "text-xs font-medium text-gray-500 uppercase tracking-wide">Active Accounts</div>
                      <div className = "text-gray-800 text-2xl font-semibold">{accounts.length}</div>
                    </div>
                  </div>
                </div>
              </div> 

              <div className = "flex gap-4 mt-4 justify-end">
              <div className = "flex flex-col w-full h-96 rounded-xl">
                    <div className = "card">
                      <h2 className = "text-gray-900 font-semibold m-6">Scheduled Payments</h2>
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

