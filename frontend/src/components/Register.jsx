import {useState} from "react"
import {userRegister, handleAPIError} from "../api/api"
import {useNavigate} from "react-router-dom"
import AuthLayout from "./AuthLayout"
import Button from '@mui/material/Button';

function Register() {
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const navigate = useNavigate()
  const [error, setError] = useState("")

  function handleRegister(e) {
    e.preventDefault()
    setError("")
    userRegister({name: name, email: email, password: password}).then(response => {
      navigate("/login")
    }).catch(err => {setError(handleAPIError(err))})
  }

  return (
    <AuthLayout>
      <div>
        <h1 className="text-sm font-semibold text-gray-700">Finance Tracker</h1>
        <h2 className="text-3xl font-semibold text-gray-900 mt-2">Create Account</h2>
        <div className="text-sm text-gray-500 mt-1">Get Started With Your Finances</div>
        <form onSubmit={handleRegister} className="flex flex-col gap-4 mt-8">
          <input className="auth-input" value={name} placeholder="Enter your name" onChange={(e) => setName(e.target.value)} />
          <input className="auth-input" value={email} placeholder="Enter your email" onChange={(e) => setEmail(e.target.value)} />
          <input className="auth-input" type="password" value={password} placeholder="Enter your password" onChange={(e) => setPassword(e.target.value)} />
          <Button type="submit" variant="contained" fullWidth sx={{color: 'white', bgcolor: "rgba(172, 138, 199)", borderRadius: '9999px', py: 1.5, mt: 2, textTransform: 'none', '&:hover': { bgcolor: '#8D8AC7' }}}>Sign Up</Button>
        </form>
        <div className="text-red-400 mt-4 text-sm">{error}</div>
      </div>
    </AuthLayout>
  )
}
export default Register
