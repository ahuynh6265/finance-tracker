import {useState} from "react"
import {createBudget} from "../api/api"

function CreateBudgetModal({budgets, categories, onCreated, onClose}) {
  // run through every category, for each category run through each budget and check if the budget category id matches the category id, return all categories without a budget - prevents 409 error 
  const availableCategories = categories.filter(c => !budgets.some(b => b.category_id === c.id))
  // set the use state to the first available category return empty string if none available 
  const [category_id, setCategoryID] = useState(availableCategories[0]?.id || "")
  const [budget_limit, setBudgetLimit] = useState(100)

  function handleCreate() {
    createBudget({category_id: Number(category_id), budget_limit: Number(budget_limit)}).then(() => {
      onCreated()
    }).catch(err => console.error(err))
  }

  function guardBudget() {
    return (
      <div>
        {(Number(budget_limit) === 0 && String(budget_limit).trim().length !== 0) ? (
          <div className = "text-red-400">Budget can not be zero.</div>
        ): null}
        {(Number(budget_limit) < 0 && String(budget_limit).trim().length !== 0) ? (
          <div className = "text-red-400">Budget can not be negative.</div>
        ): null}
        {(String(budget_limit).trim().length === 0) ? (
          <div className = "text-red-400">Budget can not be left empty.</div>
        ): null}
      </div>
    )
  }

  return (
    <div className = "modal-overlay">
      <div className = "modal-content">
        <h1 className = "absolute top-4 left-4 text-gray-300 text-xl font-semibold">Create Budget</h1>
        <button className = "absolute top-4 right-4 text-white font-semibold" onClick = {onClose}>Close</button>

        <div className = "flex gap-4">
          <div className = "w-full">
            <h2 className = "text-white font-semibold">Select Category</h2>
            {availableCategories.length > 0 ? (
            <select value = {category_id} onChange = {(e) => setCategoryID(e.target.value)}>
              {availableCategories.map(category => 
              <option key = {category.id} value = {category.id}>{category.name}</option>
              )}
            </select>): (<div>No Categories Available</div>)}
            <input value = {budget_limit} placeholder = "Budget" onChange = {(e) => setBudgetLimit(e.target.value)}></input>
          </div>
        </div>

        <button className = "text-white font-semibold" disabled = {budget_limit <= 0 || String(budget_limit).trim().length === 0 || availableCategories.length === 0} onClick = {handleCreate}>Create Budget</button>
        {guardBudget()}
      </div>
    </div>
  )
}
export default CreateBudgetModal