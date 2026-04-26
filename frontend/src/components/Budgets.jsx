import {useState, useEffect} from "react"
import {getBudgets, deleteBudget, getCategories, getBudgetsChart, refreshData, handleAPIError} from "../api/api"
import { ResponsiveContainer, BarChart, XAxis, YAxis, CartesianGrid, Tooltip, Bar } from 'recharts'
import BudgetModal from "./BudgetModal"
import Button from '@mui/material/Button';
import AddIcon from '@mui/icons-material/Add';
import DeleteIcon from '@mui/icons-material/Delete';
import IconButton from '@mui/material/IconButton';
import EditIcon from '@mui/icons-material/Edit';
import {Tooltip as MuiTooltip} from '@mui/material';
import WarningIcon from '@mui/icons-material/Warning';
import ErrorIcon from '@mui/icons-material/Error';
import CheckIcon from '@mui/icons-material/Check';
import PieChartOutlinedIcon from '@mui/icons-material/PieChartOutlined';

function Budgets() {
  const [budgets, setBudgets] = useState(null)
  const [budgetsChart, setBudgetsChart] = useState(null)
  const [categories, setCategories] = useState(null)  
  const [selectedCategoryID, setSelectedCategoryID] = useState(null)
  const [current_id, setID] = useState(null)
  const [showCreate, setShowCreate] = useState(false)
  const [error, setError] = useState("")

  useEffect (() => {
    refreshData(getBudgets, setBudgets)
    refreshData(getCategories, setCategories)
    refreshData(getBudgetsChart, setBudgetsChart).then((data) => setSelectedCategoryID(data[0]?.category_id || null))
  }, [])

  function handleDelete(budget_id){
    setError("")
    deleteBudget(budget_id).then(() => refreshData(getBudgets, setBudgets)).catch(err => {setError(handleAPIError(err))})
  }

  if (!budgets || !categories ||!budgetsChart) return <div>Loading...</div>
  else {
    let chartTotals = []
    const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    const findCategory = budgetsChart.find(c => c.category_id === Number(selectedCategoryID))
    chartTotals = (findCategory ? (
      budgetsChart.find(c => c.category_id === Number(selectedCategoryID)).monthly_totals.map((totals, i) => ({
        month: months[i], 
        totals: Number(totals)
      }))
    ) : [])

    const copyBudgets = budgets.toSorted((a, b) => Number(a.remaining_balance) - Number(b.remaining_balance))

    return (
      <div>
        <div className = "flex flex-col gap-4 h-[calc(100vh-4rem)]">
          <div className = "card">
            <div className = "p-4 flex justify-between items-center">
              <div className = "font-semibold text-gray-700">Monthly Spending</div>
              <div className = "flex flex-row items-center">
                <div className = "font-semibold text-gray-700 mr-2">Category: </div>
                <select className ="filter-select" value = {selectedCategoryID} onChange = {(e) => setSelectedCategoryID(e.target.value)}>
                  {budgetsChart.map(category =>
                    <option key = {category.category_id} value = {category.category_id}>{category.category_name}</option>
                  )}
                </select>
              </div>
            </div>
            <div className = "p-5">
              <ResponsiveContainer
              width="100%" aspect={1.618} maxHeight={350}>
              <BarChart
              data = {chartTotals}
              margin={{
                top: 5,
                right: 20,
                left: 20,
                bottom: 5,
              }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis width={60} tickFormatter={(value) => `$${value}`}/>
                <Tooltip formatter={(value) => `$${Number(value).toFixed(2)}`}/>
                <Bar name="Total Spent" dataKey="totals"  fill="#a855f7"/>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className = "card flex flex-col overflow-hidden">
            {budgets.length !== 0 ? (<>
              <div className = "flex justify-between items-center p-4">
              <div>Budgets by Category</div>
              <Button variant ="contained" sx={{color: '#a855f7', bgcolor: "#E9E8ED", '&:hover': { bgcolor: '#AFAEB0' }}} startIcon ={<AddIcon/>} onClick = {(e) => setShowCreate(true)}>Create Budget</Button>
            </div>
            <div className = "flex-1 min-h-0 overflow-y-auto px-4 pb-4">
              <table className = "transactions-table">
                <thead>
                  <tr>
                    <th>Category</th>
                    <th>Monthly Limit</th>
                    <th>Current Spent</th>
                    <th>Remaining This Month</th>
                    <th className = "w-80">Status</th>
                    <th className = "w-32">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {copyBudgets.map(budget =>
                    <tr key = {budget.id}>
                      <td>{categories.find(c => c.id === budget.category_id)?.name || "Unknown"}</td>
                      <td>${Number(budget.budget_limit).toFixed(2)}</td>
                      <td>${Number(budget.current_total).toFixed(2)}</td>
                      <td>${Number(budget.remaining_balance).toFixed(2)}</td>
                      <td>
                        {Number(budget.current_total) > Number(budget.budget_limit) 
                        ? (<div className = "text-red-600 flex items-center">
                            <ErrorIcon/>
                            <div>You are over the budget!</div>
                          </div>) 
                        : (Number(budget.current_total) > Number(budget.budget_limit) * .8) 
                          ? (<div className = "text-yellow-600 flex items-center">
                            <WarningIcon/> 
                            <div>You are close to your budget limit.</div>
                            </div>) 
                          : <div className = "text-green-600 flex items-center">
                            <CheckIcon/>
                            <div>Good this month.</div>
                            </div>}
                      </td>
                      <td>
                        <MuiTooltip title = "Delete">
                          <IconButton className ="mr-2" onClick = {() => handleDelete(budget.id)}><DeleteIcon/></IconButton>
                        </MuiTooltip>
                        <MuiTooltip title = "Edit">
                          <IconButton onClick = {() => {setID(budget.id)}}><EditIcon/></IconButton>
                        </MuiTooltip>
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div></>
            ) : (<>
            <div className = "h-full flex flex-col items-center justify-center gap-3 p-8">
              <div className = "w-14 h-14 rounded-full bg-purple-100 flex items-center justify-center">
                <PieChartOutlinedIcon sx={{ fontSize: 28, color: '#a855f7' }} />
              </div>
              <div className ="text-gray-800 font-semibold">No budgets yet</div>
              <div className ="text-gray-500 text-sm text-center max-w-xs">Create a budget to start tracking your spending by category.</div>
              <Button variant ="contained" sx={{color: '#a855f7', bgcolor: "#E9E8ED", '&:hover': { bgcolor: '#AFAEB0' }}} startIcon ={<AddIcon/>} onClick = {(e) => setShowCreate(true)}>Create Budget</Button>
            </div>
            </>)}
          </div>

        </div>
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
        <div className = "text-red-400">{error}</div>
      </div>
    )
  }
}
export default Budgets