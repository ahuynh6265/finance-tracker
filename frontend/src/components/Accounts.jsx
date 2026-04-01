import {useState, useEffect} from "react"
import {getAccounts, deleteAccount, updateAccount} from "../api/api"
import CreateAccountModal from "./CreateAccountModal"

function Accounts() {
  const [accounts, setAccounts] = useState(null)

  const [current_id, setID] = useState(null)
  const [newBank, setNewBank] = useState("")
  const [newAccountType, setNewAccountType] = useState("checking")
  const [newBalance, setNewBalance] = useState(0)

  const [showCreate, setShowCreate] = useState(false)

  useEffect (() => {
    getAccounts().then(response => {
      setAccounts(response.data)
    }).catch(err => console.error(err))
  }, [])

  function handleDelete(account_id) {
    deleteAccount(account_id).then(() => getAccounts().then(response => {
      setAccounts(response.data)
    }).catch(err => console.error(err)))
  }

  function handleUpdate(account_id) {
    updateAccount(account_id, {bank_name: newBank, account_type: newAccountType, balance: newBalance}).then(() => getAccounts().then(response => {
      setAccounts(response.data)
      setID(null)
      setNewBank("")
      setNewAccountType("checking")
      setNewBalance(0)
    }).catch(err => console.error(err)))
  }

  if (!accounts) return <div>Loading...</div>
  else return (
    <div>
      <button className = "text-white" onClick = {(e) => setShowCreate(true)}>Add Account</button>
      {showCreate ? (
        <CreateAccountModal
        onCreated = {() => {
          getAccounts().then(response => setAccounts(response.data))
          setShowCreate(false)
        }}
        onClose = {() => setShowCreate(false)}
        />
      ): null}

      {current_id ? (
        <div className = "modal-overlay">
        <div className = "modal-content">
          <h1 className = "absolute top-4 left-4 text-gray-300 text-xl font-semibold">Edit Bank Account</h1>
          <button className = "absolute top-4 right-4 text-white font-semibold" onClick = {(e) => setID(null)}>Close</button>

          <div className = "flex gap-4">
            <div className = "w-full">
              <input className = "modal-input" placeholder = "Enter Bank Name" value = {newBank} onChange = {(e) => setNewBank(e.target.value)}></input>
            </div>
          </div>

          <div className = "flex gap-4">
            <div className = "w-full">
              <h2 className = "text-white font-semibold">Select Account Type</h2>
              <select className = "modal-input" value = {newAccountType} onChange = {(e) => setNewAccountType(e.target.value)}>
              <option value = "checking">Checking</option> 
              <option value = "savings">Saving</option> 
              <option value = "credit">Credit</option> 
              </select>
            </div>
            <div className = "w-full">
              <h2 className = "text-white font-semibold">Enter Balance</h2>
              <input className = "modal-input" value = {newBalance} onChange = {(e) => setNewBalance(e.target.value)}></input> 
            </div>
          </div>

          <button className = "text-white font-semibold" onClick = {(e) => handleUpdate(current_id)}>Save Changes</button>
        </div>
      </div>
      ): null}

      <div className = "flex gap-4 mt-6">
        <div className = "border border-solid w-[55%] rounded-xl">
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
                    <button onClick = {() => {setID(account.id); setNewBank(account.bank_name); setNewAccountType(account.account_type); setNewBalance(account.balance)}}>Edit</button>
                  </div>
                  
                </div>
              </div>
            )}
          </div>
        </div>
      
        <div className = "flex flex-col w-[45%] gap-6">
          <div className = "card p-4">
            <div className = "text-white text-sm">Total Balance</div>
            <div className = "text-white text-2xl">${accounts.reduce((sum, a) => sum + a.balance, 0).toFixed(2)}</div>
          </div>
          <div className = "card p-4">
            <div className = "text-white text-sm">Active Accounts</div>
            <div className = "text-white text-2xl">{accounts.length}</div>
          </div>
        </div>
      </div> 

      <div className = "flex gap-4 mt-4 justify-end">
        <div className = "flex flex-col w-[55%] h-96 rounded-xl">
            <div className = "card">
              <h2 className = "text-white font-semibold m-6">Balance Overview</h2>
              <div></div>
            </div>
        </div>
      </div>
    </div>
  )
}

export default Accounts

