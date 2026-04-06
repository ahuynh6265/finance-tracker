import {useState, useEffect} from "react"
import {getBudgets, deleteBudget, getCategories, refreshData} from "../api/api"
import BudgetModal from "./BudgetModal"

function Budgets() {
  const [budgets, setBudgets] = useState(null)
  const [categories, setCategories] = useState(null)  
  const [current_id, setID] = useState(null)
  const [showCreate, setShowCreate] = useState(false)
  const [error, setError] = useState("")
  useEffect (() => {
    refreshData(getBudgets, setBudgets)
    refreshData(getCategories, setCategories)
  }, [])

  function handleDelete(budget_id){
    setError("")
    deleteBudget(budget_id).then(() => refreshData(getBudgets, setBudgets)).catch(err => {
      if (err.response) {
        setError(err.response.data.detail)
      }
      else {
        setError("Something went wrong.")
      }
    })
  }

  if (!budgets || !categories) return <div>Loading...</div>
  else return (
    <div>
      <button className = "text-white font-semibold" onClick = {(e) => setShowCreate(true)}>Create Budget</button> 
      {showCreate ? (
        <BudgetModal
        budget = {null}
        budgets = {budgets}
        categories = {categories}
        onSuccess = {() => {
          refreshData(getBudgets, setBudgets)
          setShowCreate(false)
        }}
        onClose = {() => setShowCreate(false)}
        />
      ): null}

      {current_id ? (
        <BudgetModal
        budget = {budgets.find (b => b.id === current_id)}
        budgets = {budgets}
        categories = {categories}
        onSuccess = {() => {
          refreshData(getBudgets, setBudgets)
          setID(null)
        }}
        onClose = {() => setID(null)}
        />
      ): null}

      <div>
        {budgets.map(budget => 
          <div key = {budget.id}>
            <div>{categories.find(c => c.id  === budget.category_id)?.name || "Unknown"}</div>
            <div>{budget.current_total}</div>
            <div>{budget.budget_limit}</div>
            <button onClick = {() => handleDelete(budget.id)}>Delete</button>
            <button onClick = {() => {setID(budget.id)}}>Edit</button> 
          </div>
        )}
      </div>
      <div className = "text-red-400">{error}</div>
    </div>
  )
}
export default Budgets