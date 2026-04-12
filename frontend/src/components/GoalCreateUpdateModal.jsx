import {useState} from "react"
import {createGoal, updateGoal, handleAPIError} from "../api/api"

function GoalCreateUpdateModal({goal, onSuccess, onClose}) {
  const [error, setError] = useState("")
  const [name, setName] = useState(goal ? goal.name : "")
  const [target_amount, setTargetAmount] = useState(goal ? goal.target_amount : 0)
  const [deadline, setDeadline] = useState(goal ? goal.deadline : "") 

  function handleSubmit() {
    setError("")
    if (isNaN(Number(target_amount))) {
      setError("Please enter a numerical value.")
    }
    else if (deadline === ""){
      setError("Please select a date.")
    }
    else if (goal === null) {
      createGoal({name: name, target_amount: Number(target_amount), deadline: deadline}).then(() => {
        onSuccess()
      }).catch(err => setError(handleAPIError(err)))
    }
    else {
      updateGoal(goal.id, {name: name, target_amount: Number(target_amount), deadline: deadline}).then(() => {
        onSuccess()
      }).catch(err => setError(handleAPIError(err)))
    }
  }
  return (
    <div className = "modal-overlay">
      <div className = "modal-content">
        {goal ? (<h1 className = "absolute top-4 left-4 text-gray-300 text-xl font-semibold">Edit Goal</h1>) : (<h1 className = "absolute top-4 left-4 text-gray-300 text-xl font-semibold">Create New Goal</h1>)}
        <button className = "absolute top-4 right-4 text-white font-semibold" onClick = {onClose}>Close</button>

        <div className = "flex gap-4">
          <div className = "w-full">
            <input className = "modal-input" placeholder = "name" value = {name} onChange = {(e) => setName(e.target.value)}></input>
            <input className = "modal-input" placeholder = "target amount" value = {target_amount} onChange = {(e) => setTargetAmount(e.target.value)}></input>
            <input className = "modal-input" type = "date" placeholder = "deadline" value = {deadline} onChange = {(e) => setDeadline(e.target.value)}></input>
          </div>
        </div>

        {goal ? (<button className = "text-white font-semibold" onClick = {handleSubmit}>Save</button>) : (<button className = "text-white font-semibold" onClick = {handleSubmit}>Create</button>)}
        <div className = "text-red-400">{error}</div>
      </div>
    </div>
  )
}
export default GoalCreateUpdateModal