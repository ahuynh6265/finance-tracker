import {useState} from "react"
import {updateBudget} from "../api/api"

function EditBudgetModal({budget, categories, onUpdated, onClose}) {
  const [newBudgetLimit, setNewBudgetLimit] = useState(budget.budget_limit)
  const [error, setError] = useState("")

  function handleUpdate() {
    setError("")
    if (isNaN(Number(newBudgetLimit))) {
      setError("Please enter a numerical value.")
    }
    else {
      updateBudget(budget.id, {budget_limit: Number(newBudgetLimit)}).then(() => {
        onUpdated()
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
        <h1>Edit Budget</h1>
        <button onClick = {onClose}>Close</button> 

        <div>
          <div>
            <div>{categories.find(c => c.id === budget.category_id)?.name || "Unknown"}</div>
            <input value = {newBudgetLimit} placeholder = "Budget" onChange = {(e) => setNewBudgetLimit(e.target.value)}></input>
          </div>
        </div>

        <button className = "text-white font-semibold" onClick = {handleUpdate}>Save</button>
        <div className = "text-red-400">{error}</div>
      </div>
    </div>
  )
}
export default EditBudgetModal