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
    <div>
      <div className = "page-title">Welcome, Alex</div>
      <div className = "banner"></div>
      <div className = "grid-layout">
        <div className = "card row-span-3">My Accounts</div>
        <div className = "col-span-2 stats-row">
          <div className = "text-green-400 text-sm card">Total Income: 
            <div className = "text-green-400 text-2xl">${summary.income}</div>
          </div>
          <div className = "text-red-400 text-sm card">Total Expenses: 
          <div className = "text-red-400 text-2xl">${summary.expenses}</div>
          </div>
          <div className =  "text-white text-sm card">Net Balance: 
            <div className = "text-white text-2xl">${summary["net balance"]}</div>
          </div>
        </div> 
        <div className = "card col-span-2 row-span-2">Balance Overview</div>
      </div>

    </div>
  )
}

export default Summary 
