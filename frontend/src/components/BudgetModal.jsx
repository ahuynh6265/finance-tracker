import {useState} from "react"
import {createBudget, updateBudget, handleAPIError} from "../api/api"

function BudgetModal({budget, budgets, categories, onSuccess, onClose}) {
  const [error, setError] = useState("")
  // run through every category, for each category run through each budget and check if the budget category id matches the category id, return all categories without a budget - prevents 409 error 
  const availableCategories = categories.filter(c => !budgets.some(b => b.category_id === c.id))
  // set the use state to the first available category return empty string if none available 
  const [category_id, setCategoryID] = useState(availableCategories[0]?.id || "")
  const [budget_limit, setBudgetLimit] = useState(budget ? (budget.budget_limit) : 0)

  function handleSubmit() {
    setError("")
    if (isNaN(Number(budget_limit))) {
      setError("Please enter a numerical value.")
    }
    else if (budget === null){
      createBudget({category_id: Number(category_id), budget_limit: Number(budget_limit)}).then(() => {
        onSuccess()
      }).catch(err => {setError(handleAPIError(err))})
    }
    else {
      updateBudget(budget.id, {budget_limit: Number(budget_limit)}).then(() => {
        onSuccess()
      }).catch(err => {setError(handleAPIError(err))})
    }
  }

  return (
    <div className = "modal-overlay">
      <div className = "modal-content">
        {budget ? (<h1 className = "absolute top-4 left-4 text-gray-300 text-xl font-semibold">Edit Budget</h1>) : (<h1 className = "absolute top-4 left-4 text-gray-300 text-xl font-semibold">Create Budget</h1>)}
        <button className = "absolute top-4 right-4 text-white font-semibold" onClick = {onClose}>Close</button>

        <div className = "flex gap-4">
          <div className = "w-full">
            {budget ? (
              <>
              <div>{categories.find(c => c.id === budget.category_id)?.name || "Unknown"}</div>
              <input value = {budget_limit} placeholder = "Budget" onChange = {(e) => setBudgetLimit(e.target.value)}></input></>
              ) : (<>
                <h2 className = "text-white font-semibold">Select Category</h2>{availableCategories.length > 0 ? (
                  <select value = {category_id} onChange = {(e) => setCategoryID(e.target.value)}>
                  {availableCategories.map(category => 
                  <option key = {category.id} value = {category.id}>{category.name}</option>
                )} </select>): (<div>No Categories Available</div>)}
                <input value = {budget_limit} placeholder = "Budget" onChange = {(e) => setBudgetLimit(e.target.value)}></input></>
              )
            }
          </div>
        </div>
        {budget ? (<button className = "text-white font-semibold" onClick = {handleSubmit}>Save</button>) : (<button className = "text-white font-semibold" disabled = {availableCategories.length === 0} onClick = {handleSubmit}>Create Budget</button>)}
        <div className = "text-red-400">{error}</div>
      </div>
    </div>
  )
}
export default BudgetModal