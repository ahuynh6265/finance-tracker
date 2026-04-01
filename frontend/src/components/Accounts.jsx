import {useState, useEffect} from "react"
import {getAccounts, createAccount, deleteAccount, updateAccount} from "../api/api"

function Accounts(){
  const [accounts, setAccounts] = useState(null)
  const [bank_name, setBank] = useState("")
  const [account_type, setType] = useState("checking")
  const [balance, setBalance] = useState(0)

  const [current_id, setID] = useState(null)
  const [newBank, setNewBank] = useState("")
  const [newType, setNewType] = useState("checking")
  const [newBalance, setNewBalance] = useState(0)

  const [showCreate, setShowCreate] = useState(false)

  useEffect (() => {
    getAccounts().then(response => {
      setAccounts(response.data)
    })
  }, [])

  function handleCreate() {
    createAccount({bank_name: bank_name, account_type: account_type, balance: balance}).then(() => getAccounts().then(response => {
      setAccounts(response.data)
      setBank("")
      setType("checking")
      setBalance(0)
    }))
  }

  function handleDelete(account_id) {
    deleteAccount(account_id).then(() => getAccounts().then(response => {
      setAccounts(response.data)
    }))
  }

  function handleUpdate(account_id) {
    updateAccount(account_id, {bank_name: newBank, account_type: newType, balance: newBalance}).then(() => getAccounts().then(response => {
      setAccounts(response.data)
      setID(null)
      setNewBank("")
      setNewType("checking")
      setNewBalance(0)
    }))
  }

  if (!accounts) return <div>Loading...</div>
  else return (
    <div>
      <button className = "text-white" onClick = {(e) => setShowCreate(true)}>Add Account</button>
      {showCreate ? (
        <div className = "modal-overlay">
          <div className = "modal-content">
            <input placeholder = "Enter Bank Name" value = {bank_name} onChange = {(e) => setBank(e.target.value)}></input>
            <button className = "absolute top-4 right-4 text-white font-semibold" onClick = {(e) => setShowCreate(false)}>Close</button>
            <select value = {account_type} onChange = {(e) => setType(e.target.value)}>
              <option value = "checking">Checking</option> 
              <option value = "savings">Saving</option> 
              <option value = "credit">Credit</option> 
            </select>
            <input placeholder = "Enter Balance" value = {balance} onChange = {(e) => setBalance(e.target.value)}></input> 
            <button onClick = {handleCreate}>Create Account</button>
          </div>
        </div>
      ): null}
      <div>
        <div className = "border border-solid w-1/2 rounded-xl">
          <h2 className = "text-white font-semibold m-6">Connected Cards</h2>
          <div className = "max-h-[300px] overflow-y-auto pb-2">
            {accounts.map(account =>
              <div className= "card mx-6 mb-6 p-2" key = {account.id}>
                <div className = "flex justify-between">

                  <div>
                    <div className = "text-white font-semibold">{account.bank_name}</div>
                    <div className = "text-gray-400 text-sm">{account.account_type}</div>
                    <div className = "text-white text-xl">{account.balance}</div>
                  </div>

                  <div className = "flex justify-center">
                    <button className = "mr-2" onClick = {() => handleDelete(account.id)}>Delete</button>
                    <button>Edit</button>
                  </div>
                  
                </div>
              </div>
            )}
          </div>
        </div>
      </div> 
    </div>
  )
}

export default Accounts

