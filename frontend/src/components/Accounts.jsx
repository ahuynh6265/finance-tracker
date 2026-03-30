import {useState, useEffect} from "react"
import {getAccounts, createAccount, deleteAccount, updateAccount} from "../api/api"

function Accounts(){
  const [accounts, setAccounts] = useState(null)
  const [bank, setBank] = useState("")
  const [type, setType] = useState("checking")
  const [balance, setBalance] = useState(0)

  const [current_id, setID] = useState(null)
  const [newBank, setNewBank] = useState("")
  const [newType, setNewType] = useState("checking")
  const [newBalance, setNewBalance] = useState(0)

  useEffect (() => {
    getAccounts().then(response => {
      setAccounts(response.data)
    })
  }, [])

  function handleCreate() {
    createAccount({bank_name: bank, account_type: type, balance: balance}).then(() => getAccounts().then(response => {
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
      <input placeholder = "Enter Bank Name" value = {bank} onChange = {(e) => setBank(e.target.value)}></input>
      <select value = {type} onChange = {(e) => setType(e.target.value)}>
        <option value = "checking">Checking</option> 
        <option value = "savings">Saving</option> 
        <option value = "credit">Credit</option> 
      </select>
      <input placeholder = "Enter Balance" value = {balance} onChange = {(e) => setBalance(e.target.value)}></input> 
      <button onClick = {handleCreate}>Create Bank Account</button>

      {accounts.map(account =>
        <div key = {account.id}>
          {(current_id === account.id)
          ? (
            <div> 
              <input value = {newBank} onChange = {(e) => setNewBank(e.target.value)}></input> 
              <select value = {newType} onChange = {(e) => setNewType(e.target.value)}>
                <option value = "checking">Checking</option> 
                <option value = "savings">Saving</option> 
                <option value = "credit">Credit</option> 
              </select>
              <input value = {newBalance} onChange = {(e) => setNewBalance(e.target.value)}></input> 
              <button onClick = {() => handleUpdate(account.id)}>Save Bank Account</button>
            </div>
          )
          : (
            <div>
              <div>{account.bank_name} - {account.account_type} - {account.balance}</div>
              <button onClick = {() => handleDelete(account.id)}>Delete Bank Account</button>
              <button onClick = {() => {setID(account.id); setNewBank(account.bank_name); setNewType(account.account_type); setNewBalance(account.balance)}}>Edit Bank Info</button> 
            </div> 
          )
          }
          </div>
      )}
    </div>
  )
}

export default Accounts