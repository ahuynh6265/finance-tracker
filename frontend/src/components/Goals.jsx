import {useState, useEffect} from "react"
import {getGoals, deleteGoal, getAccounts, getCategories, refreshData} from "../api/api"
import GoalCreateUpdateModal from "./GoalCreateUpdateModal"

function Goals() {
  const [goals, setGoals] = useState(null)
  const [accounts, setAccounts] = useState(null)
  const [categories, setCategories] = useState(null)
  const [showCreate, setShowCreate] = useState(false)
  const [current_id, setID] = useState(null)
  const [error, setError] = useState("")
  
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

        {current_id ? (
          <GoalCreateUpdateModal 
          goal = {goals.find (g => g.id === current_id)}
          onSuccess = {() => {
            refreshData(getGoals, setGoals)
            setID(null)
          }}
          onClose = {() => setID(null)}
          />
        ): null} 

        <div>
          {goals.map(goal =>
            <div key = {goal.id}>
              <div className = "text-white">{goal.name}</div>
              <div className = "text-white">Current Amount: ${goal.current_amount}</div>
              <div className = "text-white" >Target: ${goal.target_amount}</div>
              <div className = "text-white">Deadline: {goal.deadline}</div>
              <button onClick = {() => handleDelete(goal.id)}>Delete</button>
              <button onClick = {() => {setID(goal.id)}}>Edit</button> 
            </div>
          )}
        </div>
        <div className = "text-red-400">{error}</div>
      </div>
    )
  }
}
export default Goals 