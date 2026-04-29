import {useState} from "react"
import {createSubscription, updateSubscription, handleAPIError} from "../api/api"

function SubscriptionModal({subscription, subscriptions, accounts, categories, onSuccess, onClose}) {
  const [error, setError] = useState("")
  const [account_id, setAccountID] = useState(subscription ? subscription.account_id : accounts[0].id)
  const [category_id, setCategoryID] = useState(subscription ? subscription.category_id : categories[0].id)
  const [name, setName] = useState(subscription ? subscription.name : "")
  const [amount, setAmount] = useState(subscription ? subscription.amount : 0)
  const [next_due_date, setNextDueDate] = useState (subscription ? subscription.next_due_date : "")

  function handleSubmit() {
    setError("")
    if (subscription === null) {
      createSubscription({account_id: Number(account_id), category_id: Number(category_id), name: name, amount: Number(amount), next_due_date: next_due_date}).then(() => {
        onSuccess()
      }).catch(err => {setError(handleAPIError(err))})
    }
    else {
      updateSubscription(subscription.id, {account_id: Number(account_id), category_id: Number(category_id), name: name, amount: Number(amount), next_due_date: next_due_date}).then(() => {
        onSuccess()
      }).catch(err => {setError(handleAPIError(err))})
    }
  }

  return (
    <div className = "modal-overlay">
      <div className = "modal-content">
        {subscription ? (<h1 className = "absolute top-4 left-4 text-white text-xl font-semibold">Edit Subscription</h1>) : (<h1 className = "absolute top-4 left-4 text-white text-xl font-semibold">Create Subscription</h1>)}
        <button className = "absolute top-4 right-4 text-white font-semibold" onClick = {onClose}>Close</button>

        <div className = "flex items-center gap-4">
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

        <div className = "flex items-center gap-4">
          <div className = "w-full">
            <h2 className = "text-white font-semibold">Enter Name</h2>
            <input placeholder="Name" className ="modal-input" value = {name} onChange = {(e) => setName(e.target.value)}></input>
          </div>

          <div className = "w-full">
            <h2 className = "text-white font-semibold">Enter Amount</h2>
            <input className ="modal-input" value = {amount} onChange = {(e) => setAmount(e.target.value)}></input>
          </div>

          <div className = "w-full">
            <h2 className = "text-white font-semibold">Next Due Date</h2>
            <input type ="date" className ="modal-input" value = {next_due_date} onChange = {(e) => setNextDueDate(e.target.value)}></input>
          </div>
        </div>

        {subscription ? ( <button className = "bg-white text-purple-600 hover:bg-gray-100 font-semibold px-6 py-2 rounded-lg shadow-sm transition-colors" onClick = {handleSubmit}>Save</button>) : ( <button className = "bg-white text-purple-600 hover:bg-gray-100 font-semibold px-6 py-2 rounded-lg shadow-sm transition-colors" onClick = {handleSubmit}>Create</button>)}
        <div className = "text-red-600">{error}</div>
      </div>
    </div>
  )
}
export default SubscriptionModal