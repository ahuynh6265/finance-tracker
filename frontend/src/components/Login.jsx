import {useState} from "react"
import {userLogin, setAuthToken} from "../api/api"
import {useNavigate} from "react-router-dom"

function Login({onLogin}) {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const navigate = useNavigate()
  const [error, setError] = useState("")

  function handleLogin() {
    setError("")
    userLogin({email: email, password: password}).then(response => {
      localStorage.setItem("access", response.data.access_token)
      localStorage.setItem("refresh", response.data.refresh_token)
      localStorage.setItem("name", response.data.name)
      setAuthToken(response.data.access_token)
      onLogin(response.data.name)
      navigate("/")
    }).catch(err => {
      if (err.response) {
        if (err.response.status === 422) {
          const getError = err.response.data.detail[0].msg 
          setError(getError.split(",")[1].trim())
        }
        else {
          setError(err.response.data.detail)
        }
      }
      else {
        setError("Something went wrong.")
      }
    })
  }

  return (
    <div>
      <input className = "mr-2" value = {email} placeholder = "Email" onChange = {(e) => setEmail(e.target.value)}></input>
      <input type = "password" value = {password} placeholder = "Password" onChange = {(e) => setPassword(e.target.value)}></input>
      <button onClick = {handleLogin}>Login</button>
      <div className = "text-red-400">{error}</div>
    </div>
  )
}
export default Login