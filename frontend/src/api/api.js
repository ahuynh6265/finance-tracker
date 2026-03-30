import axios from "axios"; 

const BASE_URL = "http://localhost:8000"
const USER_ID = 6
const api = axios.create({baseURL: BASE_URL})

export const getSummary = () => api.get(`/users/${USER_ID}/summary`)

export const getAccounts = () => api.get(`/users/${USER_ID}/accounts`)
export const createAccount = (account_data) => api.post(`/users/${USER_ID}/accounts`, [account_data])
export const deleteAccount = (account_id) => api.delete(`/users/${USER_ID}/accounts/${account_id}`)
export const updateAccount = (account_id, account_data) => api.put(`/users/${USER_ID}/accounts/${account_id}`, account_data)

export const getCategories = () => api.get(`/users/${USER_ID}/categories`)
export const createCategory = (category_data) => api.post(`/users/${USER_ID}/categories`, [category_data])
export const deleteCategory = (category_id) => api.delete(`/users/${USER_ID}/categories/${category_id}`)
export const updateCategory = (category_id, category_data) => api.put(`/users/${USER_ID}/categories/${category_id}`, category_data)

export const getTransactions = () => api.get(`/users/${USER_ID}/transactions`)
export const createTransaction = (transaction_data) => api.post(`/users/${USER_ID}/transactions`, [transaction_data])
export const deleteTransaction = (transaction_id) => api.delete(`/users/${USER_ID}/transactions/${transaction_id}`)
export const updateTransaction = (transaction_id, transaction_data) => api.put(`/users/${USER_ID}/transactions/${transaction_id}`, transaction_data)

