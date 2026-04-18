import {useState} from "react"
import {userLogin, setAuthToken, handleAPIError} from "../api/api"
import {useNavigate} from "react-router-dom"
import AuthLayout from "./AuthLayout"
import Button from '@mui/material/Button';

function Login({onLogin}) {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const navigate = useNavigate()
  const [error, setError] = useState("")

  function handleLogin(e) {
    e.preventDefault()
    setError("")
    userLogin({email: email, password: password}).then(response => {
      localStorage.setItem("access", response.data.access_token)
      localStorage.setItem("refresh", response.data.refresh_token)
      localStorage.setItem("name", response.data.name)
      setAuthToken(response.data.access_token)
      onLogin(response.data.name)
      navigate("/")
    }).catch(err => {setError(handleAPIError(err))})
  }

  return (
    <AuthLayout>
      <div>
        <h1 className = "text-sm font-semibold text-gray-700">Finance Tracker</h1>
        <h2 className = "text-3xl font-semibold text-gray-900">Welcome Back!</h2>
        <div className ="text-sm text-gray-500 mt-1">We Are Happy To See You Again</div>
        <form onSubmit={handleLogin} className="flex flex-col gap-4 mt-8">
          <input className="auth-input" value={email} placeholder="Enter your email" onChange={(e) => setEmail(e.target.value)} />
          <input className="auth-input" type="password" value={password} placeholder="Enter your password" onChange={(e) => setPassword(e.target.value)} />
          <Button type="submit" variant="contained" fullWidth sx={{color: 'white', bgcolor: "rgba(172, 138, 199)", borderRadius: '9999px', py: 1.5, mt: 2, textTransform: 'none', '&:hover': { bgcolor: '#8D8AC7' }}}>Login</Button>
        </form>
        <div className = "text-red-400 mt-4 text-sm">{error}</div>
      </div>
    </AuthLayout>
  )
}
export default Login