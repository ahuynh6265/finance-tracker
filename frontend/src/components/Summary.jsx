import {useState, useEffect} from "react"
import {getSummary, getMonthlySummary, getCategories, getBudgets, getGoals, refreshData} from "../api/api"
import { ResponsiveContainer, LineChart, XAxis, YAxis, CartesianGrid, Tooltip, Line, Legend } from 'recharts'
import Button from '@mui/material/Button';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';
import AccountBalanceWalletIcon from '@mui/icons-material/AccountBalanceWallet';
import LinearProgress from '@mui/material/LinearProgress';

function Summary({name}) {
  const [summary, setSummary] = useState(null)
  const [monthlySummary, setMonthlySummary] = useState(null)
  const [budgets, setBudgets] = useState(null)
  const [categories, setCategories] = useState(null)
  const [goals, setGoals] = useState(null)
  
  useEffect (() => {
    refreshData(getSummary, setSummary)
    refreshData(getMonthlySummary, setMonthlySummary)
    refreshData(getBudgets, setBudgets)
    refreshData(getCategories, setCategories)
    refreshData(getGoals, setGoals)
  }, [])
  if (!summary || !monthlySummary || !budgets || !goals || !categories) return <div>Loading...</div> 
  else {
    let monthlySummaryCopy
    monthlySummaryCopy = monthlySummary.map(m => ({
    year: m.year, 
    month: m.month, 
    income: m.income, 
    expenses: m.expenses,
    net_balance: m.net_balance,
    displayDate: `${new Date(m.year, m.month - 1).toLocaleDateString("default", {month: "short"})} ${m.year}`
    }))
      
    
    const copyBudgets = budgets.filter(budget => 
      (Number(budget.current_total) > Number(budget.budget_limit) * .8) 
    ).toSorted((a, b) => Number(a.remaining_balance) - Number(b.remaining_balance)).slice(0,3)

    const copyGoals = goals.toSorted((a, b) => a.deadline.localeCompare(b.deadline)).slice(0,3)

    return (
    <div className="flex flex-col gap-4 h-[calc(100vh-4rem)]">
      <div className="page-title capitalize">Welcome, {name}</div>

      <div className="grid grid-cols-3 gap-4">
        <div className="card p-6 row-span-2 min-h-[300px]">
          <div>
            <div className="flex items-center gap-2 text-xs font-medium text-gray-500 uppercase tracking-wide">
              <AccountBalanceWalletIcon sx={{ fontSize: 16 }} />
              Net Worth
            </div>
            <div className="text-5xl font-semibold text-gray-900 mt-3">
              ${Number(summary["net balance"]).toFixed(2)}
            </div>
          </div>
          <div className="flex flex-col gap-2 pt-6 border-t border-white/50">
            <div className="flex justify-between text-sm">
              <span className="text-gray-500">Accounts</span>
              <span className="text-gray-800 font-medium">${Number(summary.accounts_only).toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-gray-500">Saved toward goals</span>
              <span className="text-gray-800 font-medium">${Number(summary.goals_only).toFixed(2)}</span>
            </div>
          </div>
        </div>

        <div className="col-span-2 grid grid-cols-3 gap-4">
          <div className="card p-4 min-h-[100px] flex flex-col justify-between">
            <div className="flex items-center justify-between">
              <div className="text-xs font-medium text-gray-500 uppercase tracking-wide">Income this month</div>
              <TrendingUpIcon sx={{ fontSize: 20, color: '#14b8a6' }} />
            </div>
            <div className="text-2xl font-semibold text-gray-800 mt-1">
              ${Number(monthlySummaryCopy.at(-1).income).toFixed(2)}
            </div>
          </div>

          <div className="card p-4 min-h-[100px] flex flex-col justify-between">
            <div className="flex items-center justify-between">
              <div className="text-xs font-medium text-gray-500 uppercase tracking-wide">Expenses this month</div>
              <TrendingDownIcon sx={{ fontSize: 20, color: '#e11d48' }} />
            </div>
            <div className="text-2xl font-semibold text-gray-800 mt-1">
              ${Number(monthlySummaryCopy.at(-1).expenses).toFixed(2)}
            </div>
          </div>

          <div className="card p-4 min-h-[100px] flex flex-col justify-between">
            <div className="text-xs font-medium text-gray-500 uppercase tracking-wide">Net balance this month</div>
            <div className={`text-2xl font-semibold mt-1 ${Number(monthlySummaryCopy.at(-1).net_balance) >= 0 ? 'text-emerald-600' : 'text-rose-600'}`}>
              ${Number(monthlySummaryCopy.at(-1).net_balance).toFixed(2)}
            </div>
          </div>
        </div>
        
        <div className="card p-5 col-span-2 min-h-[240px]">
          <div className="font-semibold text-gray-700 mb-2">Income vs Expenses — Last 6 Months</div>
          <ResponsiveContainer width="100%" aspect={2.5}>
            <LineChart data={monthlySummaryCopy.slice(-6)} margin={{ top: 10, right: 20, left: 10, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="displayDate" tick={{ fontSize: 12, fill: '#6b7280' }} />
              <YAxis width={60} tick={{ fontSize: 12, fill: '#6b7280' }} tickFormatter={(v) => `$${v}`} />
              <Tooltip formatter={(v) => `$${Number(v).toFixed(2)}`} contentStyle={{ borderRadius: 8, border: '1px solid #e5e7eb' }} />
              <Legend wrapperStyle={{ fontSize: 12 }} />
              <Line type="monotone" name="Income" dataKey="income" stroke="#14b8a6" strokeWidth={2} dot={false} />
              <Line type="monotone" name="Expenses" dataKey="expenses" stroke="#e11d48" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 flex-1">
        <div className="card p-5">
          <div className="flex items-center justify-between mb-3">
            <div className="font-semibold text-gray-700">Budgets at risk</div>
            <Button variant="text" href="/budgets" sx={{ color: '#a855f7', textTransform: 'none', fontSize: '0.875rem' }}>
              See all
            </Button>
          </div>
          {budgets.length === 0 ? (
            <div className="text-sm text-gray-500 py-6 text-center">No budgets yet.</div>
          ) : copyBudgets.length === 0 ? (
            <div className="text-sm text-gray-500 py-6 text-center">All budgets on track this month.</div>
          ) : (
            <div className="flex flex-col gap-4">
              {copyBudgets.map(budget => {
                const pct = Math.min(100, (Number(budget.current_total) / Number(budget.budget_limit)) * 100)
                const over = Number(budget.current_total) > Number(budget.budget_limit)
                return (
                  <div key={budget.id} className="flex flex-col gap-1.5">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-700 font-medium">{categories.find(c => c.id === budget.category_id)?.name || "Unknown"}</span>
                      <span className={over ? 'text-rose-600 font-medium' : 'text-amber-600 font-medium'}>
                        ${Number(budget.current_total).toFixed(2)} / ${Number(budget.budget_limit).toFixed(2)}
                      </span>
                    </div>
                    <LinearProgress
                      variant="determinate"
                      value={pct}
                      sx={{
                        height: 6,
                        borderRadius: 3,
                        backgroundColor: 'rgba(0,0,0,0.06)',
                        '& .MuiLinearProgress-bar': { backgroundColor: over ? '#e11d48' : '#f59e0b' }
                      }}
                    />
                  </div>
                )
              })}
            </div>
          )}
        </div>

        <div className="card p-5">
          <div className="flex items-center justify-between mb-3">
            <div className="font-semibold text-gray-700">Goals</div>
            <Button variant="text" href="/goals" sx={{ color: '#a855f7', textTransform: 'none', fontSize: '0.875rem' }}>
              See all
            </Button>
          </div>
          {goals.length === 0 ? (
            <div className="text-sm text-gray-500 py-6 text-center">No goals yet.</div>
          ) : (
            <div className="flex flex-col gap-4">
              {copyGoals.map(goal => {
                const current = Number(goal.current_amount)
                const target = Number(goal.target_amount)
                const pct = Math.min(100, (current / target) * 100)
                const funded = current >= target
                const overdue = !funded && new Date(goal.deadline) < new Date()
                const barColor = funded ? '#10b981' : overdue ? '#e11d48' : '#a855f7'
                return (
                  <div key={goal.id} className="flex flex-col gap-1.5">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-700 font-medium">{goal.name}</span>
                      <span className={`text-xs ${overdue ? 'text-rose-600 font-medium' : 'text-gray-500'}`}>
                        {funded ? 'Funded' : overdue ? `Overdue (${goal.deadline})` : `Due ${goal.deadline}`}
                      </span>
                    </div>
                    <LinearProgress
                      variant="determinate"
                      value={pct}
                      sx={{
                        height: 6,
                        borderRadius: 3,
                        backgroundColor: 'rgba(0,0,0,0.06)',
                        '& .MuiLinearProgress-bar': { backgroundColor: barColor }
                      }}
                    />
                    <div className="flex justify-between text-xs text-gray-500">
                      <span>${current.toFixed(2)} of ${target.toFixed(2)}</span>
                      <span>{pct.toFixed(0)}%</span>
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </div>
      </div>
    </div>
    )
  }
}

export default Summary