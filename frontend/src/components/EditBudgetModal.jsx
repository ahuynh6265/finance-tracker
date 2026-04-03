import {useState} from "react"
import {updateBudget} from "../api/api"

function EditBudgetModal({budget, categories, onUpdated, onClose}) {
  const [newBudgetLimit, setNewBudgetLimit] = useState(budget.budget_limit)

  function handleUpdate() {
    updateBudget(budget.id, {budget_limit: Number(newBudgetLimit)}).then(() => {
      onUpdated()
    }).catch(err => console.error(err))
  }

  function guardBudget() {
    return (
      <div>
        {(Number(newBudgetLimit) === 0 && String(newBudgetLimit).trim().length !== 0) ? (
          <div className = "text-red-400">Budget can not be zero.</div>
        ): null}
        {(Number(newBudgetLimit) < 0 && String(newBudgetLimit).trim().length !== 0) ? (
          <div className = "text-red-400">Budget can not be negative.</div>
        ): null}
        {(String(newBudgetLimit).trim().length === 0) ? (
          <div className = "text-red-400">Budget can not be left empty.</div>
        ): null}
      </div>
    )
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

        <button className = "text-white font-semibold" disabled = {newBudgetLimit <= 0 || String(newBudgetLimit).trim().length === 0} onClick = {handleUpdate}>Save</button>
        <div className = "justify-center">{guardBudget()}</div>
      </div>
    </div>
  )
}
export default EditBudgetModal