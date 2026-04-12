import {useState} from "react"
import {createTransaction} from "../api/api"

function AccountTransferModal({accounts, onSuccess, onClose}) {
  const [error, setError] = useState("")
  const [source, setSource] = useState("")
  const [destination, setDestination] = useState("")
  const [amount, setAmount] = useState(0)
  const [date, setDate] = useState("")

  function handleSubmit() {
    setError("")
    if (isNaN(Number(amount))){
      setError("Please enter a numerical value.")
    }
    else if (date === ""){
      setError("Please select a date.")
    }
    else {
      //category id, description are hardcoded because they will be overwritten - transaction type is hardcoded because this is the only transaction type an account-account transfer can be 
      createTransaction({account_id: Number(source), category_id: 1, destination_account_id: Number(destination), amount: Number(amount), transaction_type: "transfer", description: "Transfer", date:date}).then(() => {
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
        <h1 className = "absolute top-4 left-4 text-gray-300 text-xl font-semibold">Transfer Money</h1>
        <button className = "absolute top-4 right-4 text-white font-semibold" onClick = {onClose}>Close</button>

        <div className = "flex gap-4">
          <div className = "w-full">
            <h2 className = "text-white font-semibold">Transfer From</h2>
            <select className = "modal-input" value = {source} onChange = {(e) => setSource(e.target.value)}>
              <option value="">Select Account</option>
              {accounts.filter(a => a.id !== Number(destination)).map(account =>
                <option key = {account.id} value = {account.id}>{account.bank_name}</option>
              )}
            </select> 
          </div>
          <div className = "w-full">
            <h2 className = "text-white font-semibold">Transfer To</h2>
            <select className = "modal-input" value = {destination} onChange = {(e) => setDestination(e.target.value)}>
              <option value="">Select Account</option>
              {accounts.filter(a => a.id !== Number(source)).map(account =>
                <option key = {account.id} value = {account.id}>{account.bank_name}</option>
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
            <h2 className = "text-white font-semibold">Date of Transfer</h2>
            <input className = "modal-input" type = "date" value = {date} onChange = {(e) => setDate(e.target.value)}></input> 
          </div>
        </div>

        <button className = "text-white font-semibold" onClick = {handleSubmit}>Send Money</button>
        <div className = "text-red-400">{error}</div>
      </div>
    </div>
  )
}
export default AccountTransferModal
