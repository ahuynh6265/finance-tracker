import {useState, useEffect} from "react"
import {getSubscriptions, deleteSubscription, getAccounts, getCategories, refreshData, handleAPIError} from "../api/api"
import SubscriptionModal from "./SubscriptionModal"
import Button from '@mui/material/Button';
import AddIcon from '@mui/icons-material/Add';
import DeleteIcon from '@mui/icons-material/Delete';
import IconButton from '@mui/material/IconButton';
import EditIcon from '@mui/icons-material/Edit';
import {Tooltip as MuiTooltip} from '@mui/material';
import SubscriptionsIcon from '@mui/icons-material/Subscriptions';

function Subscriptions() {
  const [subscriptions, setSubscriptions] = useState(null)
  const [accounts, setAccounts] = useState(null)
  const [categories, setCategories] = useState(null)
  const [current_id, setID] = useState(null)
  const [showCreate, setShowCreate] = useState(false)
  const [error, setError] = useState("")

  useEffect (() => {
    refreshData(getSubscriptions, setSubscriptions)
    refreshData(getAccounts, setAccounts)
    refreshData(getCategories, setCategories)
  }, [])

  function handleDelete(subscription_id) {
    setError("")
    deleteSubscription(subscription_id).then(() => refreshData(getSubscriptions, setSubscriptions)).catch(err => {setError(handleAPIError(err))})
  }

  if (!subscriptions || !accounts || !categories) return <div>Loading...</div>
  else {
    const copySubscriptions = subscriptions.toSorted((a, b) => a.next_due_date.localeCompare(b.next_due_date))
    const copyCategories = categories.filter(c => c.name !== "Transfer")
    const totalMonthly = subscriptions.reduce((sum, subscription) => sum + Number(subscription.amount), 0)
    const annualProjection = totalMonthly * 12 
    return (
      <div>
        <div className = "flex flex-col gap-4 h-[calc(100vh-4rem)]">
          <div className="grid grid-cols-3 gap-4">
            <div className="card p-4 min-h-[100px] flex flex-col justify-between">
              <div className="text-xs font-medium text-gray-500 uppercase tracking-wide">Total Monthly Cost</div>
              <div className="text-2xl font-semibold text-gray-800 mt-1">${totalMonthly.toFixed(2)}</div>
            </div>

            <div className="card p-4 min-h-[100px] flex flex-col justify-between">
              <div className="text-xs font-medium text-gray-500 uppercase tracking-wide">Active Subscriptions</div>
              <div className="text-2xl font-semibold text-gray-800 mt-1">{subscriptions.length}</div>
            </div>

            <div className="card p-4 min-h-[100px] flex flex-col justify-between">
              <div className="text-xs font-medium text-gray-500 uppercase tracking-wide">Annual Projection</div>
              <div className="text-2xl font-semibold text-gray-800 mt-1">${annualProjection.toFixed(2)}</div>
            </div>
          </div>
          <div className = "card flex flex-col overflow-hidden">
            {subscriptions.length !== 0 ? (
              <>
              <div className = "flex justify-between items-center p-4">
                <div>Subscriptions</div>
                <Button variant ="contained" sx={{color: '#a855f7', bgcolor: "#E9E8ED", '&:hover': { bgcolor: '#AFAEB0' }}} startIcon ={<AddIcon/>} onClick = {(e) => setShowCreate(true)}>Create Subscription</Button>
              </div>
              <div className = "flex-1 min-h-0 overflow-y-auto px-4 pb-4">
                <table className = "transactions-table">
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>Account</th>
                      <th>Category</th>
                      <th>Amount</th>
                      <th>Next Due Date</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {copySubscriptions.map(subscription => 
                      <tr key  = {subscription.id}>
                        <td>{subscription.name}</td>
                        <td>{accounts.find(a => a.id === subscription.account_id)?.bank_name || "Unknown"}</td>
                        <td>{categories.find(c => c.id === subscription.category_id)?.name || "Unknown"}</td>
                        <td>${Number(subscription.amount).toFixed(2)}</td>
                        <td>{subscription.next_due_date}</td>
                        <td>
                          <MuiTooltip title = "Delete">
                            <IconButton className ="mr-2" onClick = {() => handleDelete(subscription.id)}><DeleteIcon/></IconButton>
                          </MuiTooltip>
                          <MuiTooltip title = "Edit">
                            <IconButton onClick = {() => {setID(subscription.id)}}><EditIcon/></IconButton>
                          </MuiTooltip>
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
              </>
            ) : (
              <>
              <div className = "h-full flex flex-col items-center justify-center gap-3 p-8">
                <div className = "w-14 h-14 rounded-full bg-purple-100 flex items-center justify-center">
                  <SubscriptionsIcon sx={{ fontSize: 28, color: '#a855f7' }} />
                </div>
                <div className ="text-gray-800 font-semibold">No subscription yet</div>
                <div className ="text-gray-500 text-sm text-center max-w-xs">Create a subscription to track recurring bills.</div>
                <Button variant ="contained" sx={{color: '#a855f7', bgcolor: "#E9E8ED", '&:hover': { bgcolor: '#AFAEB0' }}} startIcon ={<AddIcon/>} disabled = {accounts.length === 0} onClick = {(e) => setShowCreate(true)}>Create Subscription</Button>
                {accounts.length === 0 ? <div className ="text-gray-800 font-semibold">Create an account before creating a subscription.</div> : null}
              </div>
              </>
            )}
          </div>
        </div>
        {showCreate ? (
          <SubscriptionModal
          subscription = {null}
          accounts = {accounts}
          categories = {copyCategories}
          onSuccess = {() => {
            refreshData(getSubscriptions, setSubscriptions)
            setShowCreate(false)
          }}
          onClose = {() => setShowCreate(false)}
          />
        ): null}

        {current_id ? (
          <SubscriptionModal
          subscription = {subscriptions.find (s => s.id === current_id)}
          accounts = {accounts}
          categories = {copyCategories}
          onSuccess = {() => {
            refreshData(getSubscriptions, setSubscriptions)
            setID(null)
          }}
          onClose = {() => setID(null)}
          />
        ): null}
        <div className = "text-red-400">{error}</div>
      </div>
    )
  }
}
export default Subscriptions