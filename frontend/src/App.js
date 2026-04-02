import Summary from "./components/Summary"
import Accounts from "./components/Accounts"
import Transactions from "./components/Transactions"
import Login from "./components/Login"
import Register from "./components/Register"
import {BrowserRouter, Routes, Route, Link} from "react-router-dom"
import {useState} from "react"

function App (){
  const [loggedIn, setLoggedIn] = useState(false)
  const [name, setName] = useState("")

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
      <div className = "text-white capitalize">{name}</div>
  
    </div>
    <div className = "main-content">
      <Routes>
        <Route path = "/" element = {<Summary name = {name}/>}></Route>
        <Route path = "/accounts" element = {<Accounts />}></Route>
        <Route path = "/transactions" element = {<Transactions />}></Route>
      </Routes>
    </div> 
  </>
  ): (
    <div>
      <Routes>
        <Route path = "/*" element = {<Login onLogin = {(data) => {setLoggedIn(true); setName(data)}
        } />}></Route> 
        <Route path = "/register" element = {<Register />}></Route>
      </Routes>
  </div> 
  )}
  </BrowserRouter> )
}

export default App 

