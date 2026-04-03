import {useState, useEffect} from "react"
import {getBudgets, deleteBudget, getCategories, refreshData} from "../api/api"
import CreateBudgetModal from "./CreateBudgetModal"
import EditBudgetModal from "./EditBudgetModal"

function Budgets() {
  const [budgets, setBudgets] = useState(null)
  const [categories, setCategories] = useState(null)  
  const [current_id, setID] = useState(null)
  const [showCreate, setShowCreate] = useState(false)

  useEffect (() => {
    refreshData(getBudgets, setBudgets)
    refreshData(getCategories, setCategories)
  }, [])

  function handleDelete(budget_id){
    deleteBudget(budget_id).then(() => refreshData(getBudgets, setBudgets))
  }

  if (!budgets || !categories) return <div>Loading...</div>
  else return (
    <div>
      <button className = "text-white font-semibold" onClick = {(e) => setShowCreate(true)}>Create Budget</button> 
      {showCreate ? (
        <CreateBudgetModal
        budgets = {budgets}
        categories = {categories}
        onCreated = {() => {
          refreshData(getBudgets, setBudgets)
          setShowCreate(false)
        }}
        onClose = {() => setShowCreate(false)}
        />
      ): null}

      {current_id ? (
        <EditBudgetModal
        budget = {budgets.find (b => b.id === current_id)}
        categories = {categories}
        onUpdated = {() => {
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
    </div>
  )
}
export default Budgets