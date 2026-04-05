import Summary from "./components/Summary"
import Accounts from "./components/Accounts"
import Transactions from "./components/Transactions"
import Login from "./components/Login"
import Register from "./components/Register"
import Budgets from "./components/Budgets"
import {setAuthToken} from "./api/api"
import {BrowserRouter, Routes, Route, Link} from "react-router-dom"
import {useState, useEffect} from "react"

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

  return(
  <BrowserRouter>
  {loggedIn ? (
  <>
    <div className = "navbar">
      <div className = "text-white">Finance Tracker</div>
      <hr className = "line"></hr>
      <Link className = "nav-link" to = "/">Dashboard</Link>
      <Link className = "nav-link" to = "/accounts">Accounts</Link>
      <Link className = "nav-link" to = "/transactions">Transactions</Link>
      <Link className = "nav-link" to = "/budgets">Budgets</Link> 

      <hr className = "mt-auto line"></hr>
      <div className = "text-white capitalize">{name}</div>
  
    </div>
    <div className = "main-content">
      <Routes>
        <Route path = "/" element = {<Summary name = {name}/>}></Route>
        <Route path = "/accounts" element = {<Accounts />}></Route>
        <Route path = "/transactions" element = {<Transactions />}></Route>
        <Route path = "/budgets" element = {<Budgets />}></Route>
      </Routes>
    </div> 
  </>
  ): (
    <div>
      <Routes>
        <Route path = "/*" element = {<Login onLogin = {(data) => {setLoggedIn(true); setName(localStorage.getItem("name"))}
        } />}></Route> 
        <Route path = "/register" element = {<Register />}></Route>
      </Routes>
  </div> 
  )}
  </BrowserRouter> )
}

export default App 

