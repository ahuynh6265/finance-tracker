import Summary from "./components/Summary"
import Categories from "./components/Categories"
import Accounts from "./components/Accounts"
import Transactions from "./components/Transactions"
import {BrowserRouter, Routes, Route, Link} from "react-router-dom"

function App (){
  return(
  <BrowserRouter>
    <Link to = "/">Summary</Link>
    <Link to = "/categories">Categories</Link>
    <Link to = "/accounts">Accounts</Link>
    <Link to = "/transactions">Transactions</Link>

    <Routes>
      <Route path = "/" element = {<Summary />}></Route>
      <Route path = "/categories" element = {<Categories />}></Route>
      <Route path = "/accounts" element = {<Accounts />}></Route>
      <Route path = "/transactions" element = {<Transactions />}></Route>
    </Routes>
  </BrowserRouter> )
}

export default App 

