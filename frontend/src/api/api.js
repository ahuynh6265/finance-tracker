import axios from "axios"; 

const BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000"
const api = axios.create({baseURL: BASE_URL})

export const getSummary = () => api.get(`/summary`)

export const getAccounts = () => api.get(`/accounts`)
export const createAccount = (account_data) => api.post(`/accounts`, [account_data])
export const deleteAccount = (account_id) => api.delete(`/accounts/${account_id}`)
export const updateAccount = (account_id, account_data) => api.put(`/accounts/${account_id}`, account_data)

export const getCategories = () => api.get(`/categories`)
export const createCategory = (category_data) => api.post(`/categories`, [category_data])
export const deleteCategory = (category_id) => api.delete(`/categories/${category_id}`)
export const updateCategory = (category_id, category_data) => api.put(`/categories/${category_id}`, category_data)

export const getTransactions = () => api.get(`/transactions`)
export const createTransaction = (transaction_data) => api.post(`/transactions`, [transaction_data])
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
  }).catch(err => console.error(err))
}

export const getBudgets = () => api.get("/budgets")
export const createBudget = (budget_data) => api.post("/budgets", budget_data)
export const deleteBudget = (budget_id) => api.delete(`/budgets/${budget_id}`)
export const updateBudget = (budget_id, budget_data) => api.patch(`/budgets/${budget_id}`, budget_data)
