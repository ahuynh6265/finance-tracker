import {useState, useEffect} from "react"
import {getAccounts, deleteAccount} from "../api/api"
import CreateAccountModal from "./CreateAccountModal"
import EditAccountModal from "./EditAccountModal"

function Accounts() {
  const [accounts, setAccounts] = useState(null)
  const [current_id, setID] = useState(null)
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
        <EditAccountModal
        account = {accounts.find (a => a.id === current_id)}
        onUpdated = {() => {
          getAccounts().then(response => setAccounts(response.data))
          setID(null)
        }}
        onClose = {() => setID(null)}
        />
      ): null}

      <div className = "flex gap-4 mt-6">
        <div className = "border border-solid w-[55%] rounded-xl">
          <h2 className = "text-white font-semibold m-6">Connected Cards</h2>
          <div className = "h-[300px] overflow-y-auto pb-2">
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
                    <button onClick = {() => {setID(account.id)}}>Edit</button>
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

