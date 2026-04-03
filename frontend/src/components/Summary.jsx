import {useState, useEffect} from "react"
import {getSummary, refreshData} from "../api/api"

function Summary({name}) {
  const [summary, setSummary] = useState(null)
  
  useEffect (() => {
    refreshData(getSummary, setSummary)
  }, [])
  if (!summary) return <div>Loading...</div> 
  else return (
    <div>
      <div className = "page-title capitalize">Welcome, {name}</div>
      <div className = "banner"></div>
      <div className = "grid-layout">
        <div className = "card row-span-3 p-6">My Accounts</div>
        <div className = "col-span-2 stats-row">
          <div className = "text-green-400 text-sm p-6 card">Total Income: 
            <div className = "text-green-400 text-2xl">${summary.income}</div>
          </div>
          <div className = "text-red-400 text-sm p-6 card">Total Expenses: 
          <div className = "text-red-400 text-2xl">${summary.expenses}</div>
          </div>
          <div className =  "text-white text-sm p-6 card">Net Balance: 
            <div className = "text-white text-2xl">${summary["net balance"]}</div>
          </div>
        </div> 
        <div className = "card p-6 col-span-2 row-span-2">Balance Overview</div>
      </div>

    </div>
  )
}

export default Summary 
