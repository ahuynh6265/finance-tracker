import Summary from "./components/Summary"
import Accounts from "./components/Accounts"
import Transactions from "./components/Transactions"
import Login from "./components/Login"
import {BrowserRouter, Routes, Route, Link} from "react-router-dom"
import {useState} from "react"

function App (){
  const [loggedIn, setLoggedIn] = useState(false)

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

      <hr className = "mt-auto line"></hr>
      <div className = "text-white">Alex</div>
  
    </div>
    <div className = "main-content">
      <Routes>
        <Route path = "/" element = {<Summary />}></Route>
        <Route path = "/accounts" element = {<Accounts />}></Route>
        <Route path = "/transactions" element = {<Transactions />}></Route>
      </Routes>
    </div> 
  </>
  ): (
    <div>
      <Routes>
        <Route path = "/*" element = {<Login onLogin = {() => setLoggedIn(true)} />}></Route> 
      </Routes>
  </div> 
  )}
  </BrowserRouter> )
}

export default App 

