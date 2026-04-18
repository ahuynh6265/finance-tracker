import {NavLink} from "react-router-dom"

function AuthLayout({children}) {

  return (
    <div className = "login">
      <div className = "auth-card">
          <div className = "w-1/2 flex flex-col px-12 py-10">
            <div className = "pill-toggle">      
              <NavLink className = "pill" to="/login">Login</NavLink>
              <NavLink className = "pill" to="/register">Register</NavLink>           
            </div>
            <div className="flex-1 flex flex-col justify-center">{children}</div>
          </div>
          <div className="w-1/2 auth-gradient"></div>
      </div>
    </div>
  )
}
export default AuthLayout