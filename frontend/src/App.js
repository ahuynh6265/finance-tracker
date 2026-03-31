import Summary from "./components/Summary"
import Categories from "./components/Categories"
import Accounts from "./components/Accounts"
import Transactions from "./components/Transactions"
import {BrowserRouter, Routes, Route, Link} from "react-router-dom"

function App (){
  return(
  <BrowserRouter>
    <div className = "navbar">
      <div className = "text-white">Finance Tracker</div>
      <hr className = "line"></hr>
      <Link className = "nav-link" to = "/">Summary</Link>
      <Link className = "nav-link" to = "/categories">Categories</Link>
      <Link className = "nav-link" to = "/accounts">Accounts</Link>
      <Link className = "nav-link" to = "/transactions">Transactions</Link>

      <hr className = "mt-auto line"></hr>
      <div className = "text-white">Support</div>
      <div className = "text-white">Settings</div>
      <div className = "text-white">Name</div>
      
    </div>

    <div className = "main-content">
      <Routes>
        <Route path = "/" element = {<Summary />}></Route>
        <Route path = "/categories" element = {<Categories />}></Route>
        <Route path = "/accounts" element = {<Accounts />}></Route>
        <Route path = "/transactions" element = {<Transactions />}></Route>
      </Routes>
    </div> 
  </BrowserRouter> )
}

export default App 

