import {useState, useEffect} from "react"
import {getSummary} from "../api/api"

function Summary() {
  const [summary, setSummary] = useState(null)

  useEffect (() => {
    getSummary().then(response => {
      setSummary(response.data)
    })
  }, [])
  if (!summary) return <div>Loading...</div> 
  else return (
    <div className = "bg-slate-900 min-h-screen w-full flex flex-col gap-4 p-8">
      <div className = "text-green-400 text-sm p-4 bg-slate-800 rounded-lg h-fit">Total Income: {summary.income}</div>
      <div className = "text-red-400 text-sm p-4 bg-slate-800 rounded-lg h-fit">Total Expenses: {summary.expenses}</div>
      <div className = "p-4 bg-slate-800 rounded-lg h-fit">Net Balance: {summary["net balance"]}</div>
    </div> 
  )
}

export default Summary 
