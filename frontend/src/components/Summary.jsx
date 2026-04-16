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
      <div className = "page-title capitalize justify-between">Welcome, {name}</div>
      <div className = "banner"></div>
      <div className = "grid-layout">
        <div className = "card row-span-3 p-6">My Accounts</div>
        <div className = "col-span-2 stats-row">
          <div className = "text-gray-500 text-sm p-6 card">Total Income: 
            <div className = "text-green-600 text-2xl">${summary.income}</div>
          </div>
          <div className = "text-gray-500 text-sm p-6 card">Total Expenses: 
          <div className = "text-red-600 text-2xl">${summary.expenses}</div>
          </div>
          <div className =  " text-sm text-gray-500  p-6 card">Net Balance: 
            <div className = "text-2xl text-gray-900">${summary["net balance"]}</div>
          </div>
        </div> 
        <div className = " card p-6 col-span-2 row-span-2">Balance Overview</div>
      </div>

    </div>
  )
}

export default Summary 
