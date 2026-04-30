import {useState, useEffect, useMemo} from "react"
import {getGoals, getGoalsChart, deleteGoal, getAccounts, getCategories, refreshData, handleAPIError} from "../api/api"
import GoalCreateUpdateModal from "./GoalCreateUpdateModal"
import GoalFundWithdrawModal from "./GoalFundWithdrawModal"
import { ResponsiveContainer, LineChart, XAxis, YAxis, CartesianGrid, Tooltip, Line } from 'recharts'
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
import TrackChangesIcon from '@mui/icons-material/TrackChanges';

function Goals() {
  const [goals, setGoals] = useState(null)
  const [goalsChart, setGoalsChart] = useState(null)
  const [accounts, setAccounts] = useState(null)
  const [categories, setCategories] = useState(null)
  const [selectedGoalID, setSelectedGoalID] = useState(null)

  const [showCreate, setShowCreate] = useState(false)
  const [current_id, setID] = useState(null)
  const [error, setError] = useState("")
  const [mode, setMode] = useState(null)
  const [toggleTimeRange, setToggleTimeRange] = useState("biweekly")

  const copyGoals = useMemo(() => goals?.toSorted((a, b) => a.deadline.localeCompare(b.deadline)) || [], [goals])
  
  useEffect (() => {
    refreshData(getGoals, setGoals).then((data) => {
      if (data.length > 0) {
        setSelectedGoalID(data.toSorted((a, b)=> a.deadline.localeCompare(b.deadline))[0].id)
      }
    })
    refreshData(getAccounts, setAccounts)
    refreshData(getCategories, setCategories)
  }, [])

  useEffect(() => {
    if (!selectedGoalID) return
    getGoalsChart(selectedGoalID).then(response => {
      setGoalsChart(response.data)
    })
  }, [selectedGoalID])

  function handleChartUpdate(selectedGoalID) {
    getGoalsChart(selectedGoalID).then(response => {
      setGoalsChart(response.data)
    })
  }
  
  function handleDelete(goal_id) {
    setError("")
    deleteGoal(goal_id).then(() => refreshData(getGoals, setGoals)).then(() => {
      if (goal_id === Number(selectedGoalID)) {
        setSelectedGoalID(copyGoals.find(g => g.id !== goal_id)?.id || null)
      }
    }).catch(err => {setError(handleAPIError(err))})
  }

  if (!goals || !accounts || !categories) return <div>Loading...</div>
  else {
    if (goals.length === 0) {
      return(
        <div className = "h-[calc(100vh-4rem)]">
          <div className ="card h-full flex flex-col items-center justify-center gap-3 p-8">
            <div className="w-14 h-14 rounded-full bg-purple-100 flex items-center justify-center">
              <TrackChangesIcon sx={{ fontSize: 28, color: '#a855f7' }} />
            </div>
            <div className="text-gray-800 font-semibold">No goals yet</div>
            <div className="text-gray-500 text-sm text-center max-w-xs">Create a goal to start tracking your progress toward something you're saving for.</div>
            <Button variant ="contained" sx={{color: '#a855f7', bgcolor: "#E9E8ED", '&:hover': { bgcolor: '#AFAEB0' }}} startIcon ={<AddIcon/>} disabled = {accounts.length === 0} onClick = {(e) => setShowCreate(true)}>Create Budget</Button>
            {accounts.length === 0 ? <div className ="text-gray-800 font-semibold">Create an account before creating a goal.</div> : null}
          </div>
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
        </div>
      )
    }
    else {
      const handleToggle = (event, toggleTimeRange) => {
        setToggleTimeRange(toggleTimeRange)
      }
      
      const selectedGoal = copyGoals.find(g => g.id === Number(selectedGoalID)) || copyGoals[0]
      //millseconds to days
      const deadline = selectedGoal.deadline
      const [y, m, d] = deadline.split("-").map(Number)
      const localMidnight = new Date(y, m - 1, d)
      const daysToDeadline = (localMidnight - new Date().setHours(0,0,0,0)) / (1000 * 60 * 60 * 24) 

      //get date in yyyy-mm-dd to compare instead of comparing through utc
      const now = new Date()
      const year = now.getFullYear()
      const month = String(now.getMonth() + 1).padStart(2, '0')
      const day = String(now.getDate()).padStart(2, '0')
      const todayStr = `${year}-${month}-${day}`
      
      let periodLabel
      let fundRange = daysToDeadline 
      let pace
      //use math.ceil to catch deadlines that are less than the funding pace
      if (toggleTimeRange === "weekly") {
        fundRange = Math.ceil(daysToDeadline / 7)
        periodLabel = "weekly"
      }
      else if (toggleTimeRange === "biweekly") {
        fundRange = Math.ceil(daysToDeadline / 14)
        periodLabel = "biweekly"
      }
      else {
        fundRange = Math.ceil(daysToDeadline / 30)
        periodLabel = "monthly"
      }
      pace = Math.ceil(Number(selectedGoal.remaining_needed) / Number(fundRange))
      const readableDate = localMidnight.toLocaleDateString("en-US", {
        year: "numeric", 
        month: "short",
        day: "numeric"
      })

      let chartData
      if (goalsChart !== null){
        chartData = goalsChart.map(g => ({
          date: g.date.slice(5), 
          cumulative: Number(g.cumulative),
          target: Number(selectedGoal.target_amount)
        }))
      }

      return (
        <div>
          <div className = "flex flex-col gap-4 h-[calc(100vh-4rem)]">
            <div className = "flex card gap-4"> 
              <div className = "flex flex-col flex-1">
                <div className = "p-4 flex justify-between items-center">
                  <div className = "font-semibold text-gray-700">Funding Pace</div>
                </div>
      
                <div className = "flex-1 flex flex-col items-center justify-center gap-3 p-8">
                  {Number(selectedGoal.current_amount) >= Number(selectedGoal.target_amount)
                  ? (
                    <div className="flex flex-col items-center justify-center gap-3 py-4">
                      <div className="w-14 h-14 rounded-full bg-green-100 flex items-center justify-center">
                        <CheckIcon sx={{ fontSize: 28, color: '#16a34a' }} />
                      </div>
                      <div className="text-2xl font-semibold text-gray-800">Goal achieved!</div>
                      <div className="text-gray-600 text-center max-w-md">
                        You hit your <span className="font-semibold text-gray-800">${Number(selectedGoal.target_amount).toFixed(2)}</span> target for <span className="font-semibold text-gray-800">{selectedGoal.name}</span>
                      </div>
                      <div className="text-sm text-gray-500">Deadline: {readableDate}</div>
                    </div>
                  ) 
                  : (
                    Number(selectedGoal.current_amount) < Number(selectedGoal.target_amount) && selectedGoal.deadline < todayStr 
                    ? (
                      <div className="flex flex-col items-center justify-center gap-3 py-4">
                        <div className="w-14 h-14 rounded-full bg-red-100 flex items-center justify-center">
                          <ErrorIcon sx={{ fontSize: 28, color: '#dc2626' }} />
                        </div>
                        <div className="text-2xl font-semibold text-gray-800">Deadline passed</div>
                        <div className="text-gray-600 text-center max-w-md">
                          <span className="font-semibold text-gray-800">${Number(selectedGoal.remaining_needed).toFixed(2)}</span> short of your <span className="font-semibold text-gray-800">${Number(selectedGoal.target_amount).toFixed(2)}</span> target for <span className="font-semibold text-gray-800">{selectedGoal.name}</span>
                        </div>
                        <div className="text-sm text-gray-500">Was due {readableDate}</div>
                      </div>
                    ) : (<>
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
                        ${Number(selectedGoal.remaining_needed).toFixed(2)} remaining of ${Number(selectedGoal.target_amount).toFixed(2)} target · Deadline in {Math.floor(daysToDeadline)} days
                      </div>
                      </>
                    ) 
                  )}
                </div>
              </div>

              <div className = "flex flex-col flex-1">
                <div className = "flex items-center gap-4 justify-between p-4">
                  <div className="font-semibold text-gray-700">Cumulative Progress</div>
                  <div className = "flex flex-row items-center">
                    <div className = "font-semibold text-gray-700 mr-2">Goal: </div>
                    <select className = "filter-select" value = {selectedGoalID} onChange = {(e) => setSelectedGoalID(Number(e.target.value))}>
                      {copyGoals.map(goal =>
                        <option key = {goal.id} value = {goal.id}>{goal.name}</option>
                      )}
                    </select>
                  </div>
                </div>
                <div className = "flex-1 p-4 w-full">
                  {goalsChart ? (
                    <ResponsiveContainer width="100%" aspect={1.618} maxHeight={350}>
                      <LineChart
                      data = {chartData}
                      margin={{
                        top: 5,
                        right: 30,
                        left: 20,
                        bottom: 5,
                      }}
                      >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="date" />
                        <YAxis width={60} dataKey="target"/>
                        <Tooltip />
                        <Line type="monotone" name="Current amount funded" dataKey="cumulative" dot = {false} stroke="#14b8a6"/>
                      </LineChart>
                    </ResponsiveContainer>
                  ) : null}
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
                            {Number(goal.current_amount) > 0 
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
                          
                              {Number(goal.current_amount) > 0 
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
              refreshData(getGoals, setGoals).then((data) => {
                setSelectedGoalID(data.toSorted((a, b) => a.deadline.localeCompare(b.deadline))[0].id)
              })
              setShowCreate(false)
            }}
            onClose = {() => setShowCreate(false)}
            />
          ): null}
  
          {(current_id && !mode) ? (
            <GoalCreateUpdateModal
            goal = {goals.find (g => g.id === current_id)}
            onSuccess = {() => {
              refreshData(getGoals, setGoals).then((data) => {
                setSelectedGoalID(data.toSorted((a, b) => a.deadline.localeCompare(b.deadline))[0].id)
              })
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
              refreshData(getGoals, setGoals).then(() => handleChartUpdate(selectedGoalID))
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
}
export default Goals 