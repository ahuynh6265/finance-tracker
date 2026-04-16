import axios from "axios"; 

const BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000"
const api = axios.create({baseURL: BASE_URL})

export const getSummary = () => api.get(`/summary`)
export const getAccountSummary = (account_id) => api.get(`/accounts/${account_id}/summary`)
export const getAccountTransactions = (account_id) => api.get(`/accounts/${account_id}/transactions`)

export const getAccounts = () => api.get(`/accounts`)
export const createAccount = (account_data) => api.post(`/accounts`, account_data)
export const deleteAccount = (account_id) => api.delete(`/accounts/${account_id}`)
export const updateAccount = (account_id, account_data) => api.put(`/accounts/${account_id}`, account_data)

export const getCategories = () => api.get(`/categories`)
export const deleteCategoryTransactions = (category_id) => api.delete(`/categories/${category_id}/transactions`)

export const getTransactions = () => api.get(`/transactions`)
export const createTransaction = (transaction_data) => api.post(`/transactions`, transaction_data)
export const deleteTransaction = (transaction_id) => api.delete(`/transactions/${transaction_id}`)
export const updateTransaction = (transaction_id, transaction_data) => api.put(`/transactions/${transaction_id}`, transaction_data)

export const userRegister = (user_data) => api.post(`/auth/register`, user_data)
export const userLogin = (user_data) => api.post(`/auth/login`, user_data)

export const setAuthToken = (token) => {
  api.defaults.headers.common['Authorization'] = `Bearer ${token}`
}

export function refreshData(getAPI, setState) {
  return getAPI().then(response => {
    setState(response.data)
    return response.data
  }).catch(err => console.error(err))
}

export const getBudgets = () => api.get("/budgets")
export const createBudget = (budget_data) => api.post("/budgets", budget_data)
export const deleteBudget = (budget_id) => api.delete(`/budgets/${budget_id}`)
export const updateBudget = (budget_id, budget_data) => api.patch(`/budgets/${budget_id}`, budget_data)

export const getGoals = () => api.get("/goals")
export const createGoal = (goal_data) => api.post("/goals", goal_data)
export const deleteGoal = (goal_id) => api.delete(`/goals/${goal_id}`)
export const updateGoal = (goal_id, goal_data) => api.put(`/goals/${goal_id}`, goal_data)
export const fundGoal = (goal_id, update_data) => api.put(`/goals/${goal_id}/current-amount`, update_data)
export const withdrawGoal = (goal_id, update_data) => api.put(`/goals/${goal_id}/withdraw`, update_data)

export const refreshToken = (refresh_token) => api.post("/auth/refresh", {"refresh_token": refresh_token})

api.interceptors.response.use(
  response => response,
  error => {
    const status = error.response ? error.response.status : null; 
    //if refresh token is expired it will also return 401, this will prevent an infinite loop 
    //added login to if statement to prevent website refresh on user error 
    if (status === 401 && error.config.url !== "/auth/refresh" && error.config.url !== "/auth/login") {
      const refresh_token = localStorage.getItem("refresh")
      if (!refresh_token) {window.location.href = "/login"}
      else{
        return refreshToken(refresh_token).then(response => {
          localStorage.setItem("access", response.data.access_token)
          setAuthToken(response.data.access_token)
          error.config.headers["Authorization"] = `Bearer ${response.data.access_token}`
          return api(error.config)
        }).catch(() => {window.location.href = "/login"})
      }  
    }
    return Promise.reject(error)
  }
)

export function handleAPIError(err) {
  if (err.response) {
    if (err.response.status === 422) {
      const getError = err.response.data.detail[0].msg
      return getError.split(",")[1].trim()
    }
    else {
      return err.response.data.detail
    }
  }
  else {
    return "Something went wrong."
  }
}