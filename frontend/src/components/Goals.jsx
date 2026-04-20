import {useState, useEffect} from "react"
import {getGoals, deleteGoal, getAccounts, getCategories, refreshData, handleAPIError} from "../api/api"
import GoalCreateUpdateModal from "./GoalCreateUpdateModal"
import GoalFundWithdrawModal from "./GoalFundWithdrawModal"
import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';
import Button from '@mui/material/Button';
import AddIcon from '@mui/icons-material/Add';
import {Tooltip as MuiTooltip} from '@mui/material';
import ErrorIcon from '@mui/icons-material/Error';
import CheckIcon from '@mui/icons-material/Check';
import DeleteIcon from '@mui/icons-material/Delete';
import IconButton from '@mui/material/IconButton';
import EditIcon from '@mui/icons-material/Edit';
import PaidIcon from '@mui/icons-material/Paid';
import RemoveCircleIcon from '@mui/icons-material/RemoveCircle';

function Goals() {
  const [goals, setGoals] = useState(null)
  const [accounts, setAccounts] = useState(null)
  const [categories, setCategories] = useState(null)
  const [selectedGoalID, setSelectedGoalID] = useState(null)

  const [showCreate, setShowCreate] = useState(false)
  const [current_id, setID] = useState(null)
  const [error, setError] = useState("")
  const [mode, setMode] = useState(null)
  const [toggleTimeRange, setToggleTimeRange] = useState("biweekly")
  
  useEffect (() => {
    refreshData(getGoals, setGoals).then((data) => setSelectedGoalID(data[0].id))
    refreshData(getAccounts, setAccounts)
    refreshData(getCategories, setCategories)
  }, [])

  function handleDelete(goal_id) {
    setError("")
    deleteGoal(goal_id).then(() => refreshData(getGoals, setGoals)).catch(err => {setError(handleAPIError(err))})
  }

  if (!goals || !accounts || !categories) return <div>Loading...</div>
  else {
    const handleToggle = (event, toggleTimeRange) => {
      setToggleTimeRange(toggleTimeRange)
    }
    
    const selectedGoal = goals.find(g => g.id === Number(selectedGoalID));
    //millseconds to days
    const deadline = (new Date(selectedGoal.deadline) - new Date()) / (1000 * 60 * 60 * 24) 
    let periodLabel
    let fundRange = deadline 
    let pace
    if (toggleTimeRange === "weekly") {
      fundRange = deadline / 7
      periodLabel = "weekly"
    }
    else if (toggleTimeRange === "biweekly") {
      fundRange = deadline / 14
      periodLabel = "biweekly"
    }
    else {
      fundRange = deadline / 30
      periodLabel = "monthly"
    }
    pace = Math.ceil(Number(selectedGoal.remaining_needed) / Number(fundRange))
    const readableDate = new Date(selectedGoal.deadline).toLocaleDateString("en-US", {
      year: "numeric", 
      month: "short",
      day: "numeric"
    })

    //get date in yyyy-mm-dd to compare instead of comparing through utc
    const now = new Date()
    const year = now.getFullYear()
    const month = String(now.getMonth() + 1).padStart(2, '0')
    const day = String(now.getDate()).padStart(2, '0')
    const todayStr = `${year}-${month}-${day}`

    const copyGoals = goals.toSorted((a, b) => a.deadline.localeCompare(b.deadline))
  
    return (
      <div>
        <div className = "flex flex-col gap-4 h-[calc(100vh-4rem)]">
          <div className = "card flex flex-col">
            <div className = "p-4 flex justify-between items-center">
              <div className = "font-semibold text-gray-700">Funding Pace</div>
              <div className = "flex items-center gap-4">
                <div className = "flex flex-row items-center">
                  <div className = "font-semibold text-gray-700 mr-2">Goal: </div>
                  <select className = "filter-select" value = {selectedGoalID} onChange = {(e) => setSelectedGoalID(e.target.value)}>
                    {copyGoals.map(goal =>
                      <option key = {goal.id} value = {goal.id}>{goal.name}</option>
                    )}
                  </select>
                </div>
              </div>
            </div>
  
            <div className = "flex-1 flex flex-col items-center justify-center gap-3 p-8">
              <div className = "text-xs font-medium text-gray-500 uppercase tracking-wide">Need to fund</div>
              <div className="flex items-baseline gap-2">
                <div className="text-6xl font-bold text-gray-800">
                  ${Number(pace).toFixed(2)}
                </div>
                <div className="text-2xl font-medium text-gray-500">
                  {periodLabel}
                </div>
              </div>
              <div className="text-gray-600 text-center max-w-md">to reach <span className="font-semibold text-gray-800">{selectedGoal.name}</span> by {readableDate}</div>
              <ToggleButtonGroup
                value = {toggleTimeRange}
                exclusive
                onChange = {handleToggle}
                size = "small"
                sx={{mt:2}}
                >
                <ToggleButton value="weekly" sx={{ textTransform: 'none', px: 3 }}>
                  Weekly
                </ToggleButton>
                <ToggleButton value="biweekly" sx={{ textTransform: 'none', px: 3 }}>
                  Biweekly
                </ToggleButton>
                <ToggleButton value="monthly" sx={{ textTransform: 'none', px: 3 }}>
                  Monthly
                </ToggleButton>
              </ToggleButtonGroup>
              <div className="text-sm text-gray-500 mt-2">
                ${Number(selectedGoal.remaining_needed).toFixed(2)} remaining of ${Number(selectedGoal.target_amount).toFixed(2)} target · Deadline in {Math.floor(deadline)} days
              </div>
            </div>
          </div>

          <div className = "card flex flex-col overflow-hidden">
            {goals.length !== 0 ? (
              <>
              <div className = "flex justify-between items-center p-4">
                <div>Goals</div>
                <Button variant ="contained" sx={{color: '#D1B0F5', bgcolor: "#E9E8ED", '&:hover': { bgcolor: '#AFAEB0' }}} startIcon ={<AddIcon/>} onClick = {(e) => setShowCreate(true)}>Create Goal</Button>
              </div>
              <div className = "flex-1 min-h-0 overflow-y-auto px-4 pb-4">
                <table className = "transactions-table">
                  <thead>
                    <tr>
                      <th>Goal Name</th>
                      <th>Deadline</th>
                      <th>Target Amount</th>
                      <th>Current Amount</th>
                      <th className = "w-96">Status</th>
                      <th className = "w-40">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {copyGoals.map(goal =>
                      <tr key = {goal.id}>
                        <td>{goal.name}</td>
                        <td>{goal.deadline}</td>
                        <td>{Number(goal.target_amount).toFixed(2)}</td>
                        <td>{Number(goal.current_amount).toFixed(2)}</td>
                        <td>
                          {(Number(goal.current_amount) >= Number(goal.target_amount)) 
                          ? (
                            <div className = "text-green-600 flex items-center">
                              <CheckIcon/>
                              <div>Goal achieved!</div>
                            </div>
                          ) 
                          : (
                            goal.deadline < todayStr && Number(goal.current_amount) < Number(goal.target_amount) 
                            ? (
                              <div className = "text-red-600 flex items-center">
                                <ErrorIcon/>
                                <div>Deadline has passed — ${Number(goal.remaining_needed).toFixed(2)} short </div>
                              </div>
                            ) 
                            : (
                              <div>On Track</div>
                            )
                          )}
                        </td>
                        <td>
                          {goal.current_amount > 0 
                          ? null 
                          : (
                            <MuiTooltip title = "Delete">
                              <IconButton className ="mr-2" onClick = {() => handleDelete(goal.id)}><DeleteIcon/></IconButton>
                            </MuiTooltip>
                          )}
                            <MuiTooltip title = "Edit">
                              <IconButton onClick = {() => {setID(goal.id)}}><EditIcon/></IconButton>
                            </MuiTooltip> 

                            <MuiTooltip title = "Fund">
                            <IconButton onClick = {() => {setID(goal.id); setMode("fund")}}><PaidIcon/></IconButton>
                            </MuiTooltip> 
                        
                            {goal.current_amount > 0 
                            ? (
                              <MuiTooltip title = "Withdraw">
                                <IconButton onClick = {() => {setID(goal.id); setMode("withdraw")}}><RemoveCircleIcon/></IconButton>
                              </MuiTooltip>
                            ) 
                            : null}
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
              </>
            ) : null}
          </div>
        </div>
        <div className = "text-red-400">{error}</div>

        {showCreate ? (
          <GoalCreateUpdateModal 
          goal = {null}
          onSuccess = {() => {
            refreshData(getGoals, setGoals)
            setShowCreate(false)
          }}
          onClose = {() => setShowCreate(false)}
          />
        ): null}

        {(current_id && !mode) ? (
          <GoalCreateUpdateModal 
          goal = {goals.find (g => g.id === current_id)}
          onSuccess = {() => {
            refreshData(getGoals, setGoals)
            setID(null)
          }}
          onClose = {() => setID(null)}
          />
        ): null} 

        {mode ? (
          <GoalFundWithdrawModal 
          goal = {goals.find (g => g.id === current_id)}
          mode = {mode}
          accounts = {accounts}
          onSuccess = {() => {
            refreshData(getGoals, setGoals)
            setID(null)
            setMode(null)
          }}
          onClose = {() => {setID(null); setMode(null)}}
          />
        ) : null}
      </div>
    )
  }
}
export default Goals 