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
        {budget ? (<h1 className = "absolute top-4 left-4 text-white text-xl font-semibold">Edit Budget</h1>) : (<h1 className = "absolute top-4 left-4 text-white text-xl font-semibold">Create Budget</h1>)}
        <button className = "absolute top-4 right-4 text-white font-semibold" onClick = {onClose}>Close</button>

        <div className = "flex items-center gap-4">
          <div className = "w-full">
            {budget ? (
              <>
              <h2 className = "text-white font-semibold">{categories.find(c => c.id === budget.category_id)?.name || "Unknown"}</h2>
              <input className = "modal-input" value = {budget_limit} placeholder = "Budget" onChange = {(e) => setBudgetLimit(e.target.value)}></input></>
              ) : (<>
                <h2 className = "text-white font-semibold">Select Category</h2>{availableCategories.length > 0 ? (
                  <select className = "modal-input" value = {category_id} onChange = {(e) => setCategoryID(e.target.value)}>
                  {availableCategories.map(category =>
                  <option key = {category.id} value = {category.id}>{category.name}</option>
                )} </select>): (<div className = "text-white">No Categories Available</div>)}
                <div className = "w-full">
                  <h2 className = "text-white font-semibold">Enter Budget Limit</h2>
                  <input className = "modal-input" value = {budget_limit} placeholder = "Budget" onChange = {(e) => setBudgetLimit(e.target.value)}></input>
              </div>
              </>
              )
            }
          </div>
        </div>
        {budget ? (<button className = "bg-white text-purple-600 hover:bg-gray-100 font-semibold px-6 py-2 rounded-lg shadow-sm transition-colors" onClick = {handleSubmit}>Save</button>) : (<button className = "bg-white text-purple-600 hover:bg-gray-100 font-semibold px-6 py-2 rounded-lg shadow-sm transition-colors" disabled = {availableCategories.length === 0} onClick = {handleSubmit}>Create</button>)}
        <div className = "text-red-400">{error}</div>
      </div>
    </div>
  )
}
export default BudgetModal