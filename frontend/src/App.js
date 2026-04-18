import Summary from "./components/Summary"
import Accounts from "./components/Accounts"
import Transactions from "./components/Transactions"
import Login from "./components/Login"
import Register from "./components/Register"
import Budgets from "./components/Budgets"
import Goals from "./components/Goals"
import {setAuthToken} from "./api/api"
import {BrowserRouter, Routes, Route, NavLink, Navigate} from "react-router-dom"
import {useState, useEffect} from "react"
import { MdOutlineAccountBalanceWallet, MdOutlinePayments, MdOutlineHome } from "react-icons/md"
import { GoGoal } from "react-icons/go"
import { IoPieChartOutline } from "react-icons/io5";
import { CiLogout } from "react-icons/ci";

function App (){
  const [loggedIn, setLoggedIn] = useState(false)
  const [name, setName] = useState("")

  useEffect (() => {
    const access_token = localStorage.getItem("access")
    const refresh_token = localStorage.getItem("refresh")

    if (access_token && refresh_token) {
      setLoggedIn(true)
      setName(localStorage.getItem("name"))
      setAuthToken(access_token)
    } 
  }, [])

  function logOut() {
    localStorage.removeItem("access")
    localStorage.removeItem("refresh")
    localStorage.removeItem("name")
    setLoggedIn(false)
  }

  return(
  <BrowserRouter>
  {loggedIn ? (
  <>
    <div className = "navbar">
      <div className = "text-gray-800 font-bold">Finance Tracker</div>
      <hr className = "line"></hr>
      <NavLink className = "nav-link" to = "/"><MdOutlineHome/>Dashboard</NavLink>
      <NavLink  className = "nav-link" to = "/accounts"><MdOutlineAccountBalanceWallet/>Accounts</NavLink>
      <NavLink className = "nav-link" to = "/transactions"><MdOutlinePayments/>Transactions</NavLink>
      <NavLink className = "nav-link" to = "/budgets"><IoPieChartOutline/>Budgets</NavLink> 
      <NavLink className = "nav-link" to = "/goals"><GoGoal/>Goals</NavLink>

      <hr className = "mt-auto line"></hr>
      <div className = "capitalize">{name}</div>
      <button className = "text-left flex items-center gap-2" onClick = {logOut}><CiLogout/>Sign Out</button>
  
    </div>
    <div className = "main-content">
      <Routes>
        <Route path = "/" element = {<Summary name = {name}/>}></Route>
        <Route path = "/accounts" element = {<Accounts />}></Route>
        <Route path = "/transactions" element = {<Transactions />}></Route>
        <Route path = "/budgets" element = {<Budgets />}></Route>
        <Route path = "/goals" element = {<Goals />}></Route>
      </Routes>
    </div> 
  </>
  ): (
    <div>
      <Routes>
        <Route path = "/login" element = {<Login onLogin = {(data) => {setLoggedIn(true); setName(localStorage.getItem("name"))}
        } />}></Route> 
        <Route path = "/register" element = {<Register />}></Route>
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
  </div> 
  )}
  </BrowserRouter> )
}

export default App 

