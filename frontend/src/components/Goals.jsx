import {useState, useEffect} from "react"
import {getGoals, deleteGoal, getAccounts, getCategories, refreshData} from "../api/api"
import GoalCreateUpdateModal from "./GoalCreateUpdateModal"
import GoalFundWithdrawModal from "./GoalFundWithdrawModal"

function Goals() {
  const [goals, setGoals] = useState(null)
  const [accounts, setAccounts] = useState(null)
  const [categories, setCategories] = useState(null)
  const [showCreate, setShowCreate] = useState(false)
  const [current_id, setID] = useState(null)
  const [error, setError] = useState("")
  const [mode, setMode] = useState(null)
  
  useEffect (() => {
    refreshData(getGoals, setGoals)
    refreshData(getAccounts, setAccounts)
    refreshData(getCategories, setCategories)
  }, [])

  function handleDelete(goal_id) {
    setError("")
    deleteGoal(goal_id).then(() => refreshData(getGoals, setGoals)).catch(err => {
      if (err.response) {
        setError(err.response.data.detail)
      }
      else {
        setError("Something went wrong.")
      }
    })
  }

  if (!goals || !accounts || !categories) return <div>Loading...</div>
  else {
    return (
      <div>
        <button className = "text-white" onClick = {(e) => setShowCreate(true)}>Create Goal</button>
        {showCreate ? (
          <GoalCreateUpdateModal 
          goal = {null}
          onSuccess = {() => {
            refreshData(getGoals, setGoals)
            setShowCreate(false)
          }}
          onClose = {() => setShowCreate(false)}
          />
        ): null}

        {(current_id && !mode) ? (
          <GoalCreateUpdateModal 
          goal = {goals.find (g => g.id === current_id)}
          onSuccess = {() => {
            refreshData(getGoals, setGoals)
            setID(null)
          }}
          onClose = {() => setID(null)}
          />
        ): null} 

        {mode ? (
          <GoalFundWithdrawModal 
          goal = {goals.find (g => g.id === current_id)}
          mode = {mode}
          accounts = {accounts}
          onSuccess = {() => {
            refreshData(getGoals, setGoals)
            setID(null)
            setMode(null)
          }}
          onClose = {() => {setID(null); setMode(null)}}
          />
        ) : null}

        <div>
          {goals.map(goal =>
            <div key = {goal.id}>
              <div className = "text-white">{goal.name}</div>
              <div className = "text-white">Current Amount: ${goal.current_amount}</div>
              <div className = "text-white" >Target: ${goal.target_amount}</div>
              <div className = "text-white">Deadline: {goal.deadline}</div>
              {(goal.current_amount > 0) ? (null) : (<button onClick = {() => handleDelete(goal.id)}>Delete</button>)}
              <button onClick = {() => {setID(goal.id)}}>Edit</button> 
              <button onClick = {() => {setID(goal.id); setMode("fund")}}>Fund</button>
              {(goal.current_amount > 0) ? (<button onClick = {() => {setID(goal.id); setMode("withdraw")}}>Withdraw</button>) : null}
            </div>
          )}
        </div>
        <div className = "text-red-400">{error}</div>
      </div>
    )
  }
}
export default Goals 