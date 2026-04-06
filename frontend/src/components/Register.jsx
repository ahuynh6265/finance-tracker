import {useState} from "react"
import {userRegister} from "../api/api"
import {useNavigate} from "react-router-dom"

function Register() {
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const navigate = useNavigate()
  const [error, setError] = useState("")

  function handleRegister() {
    setError("")
    userRegister({name: name, email: email, password: password}).then(response => {
      navigate("/login")
    }).catch(err => {
      if (err.response){
        if (err.response.status === 422) {
          const getError = err.response.data.detail[0].msg 
          setError(getError.split(",")[1].trim())
        }
        else {
          (setError(err.response.data.detail))
        }
      }
      else {
        setError ("Something went wrong.")
      }
    })
  }

  return (
    <div>
      <input value = {name} placeholder = "Name" onChange = {(e) => setName(e.target.value)}></input>
      <input value = {email} placeholder = "Email" onChange = {(e) => setEmail(e.target.value)}></input>
      <input type = "password" value = {password} placeholder = "Password" onChange = {(e) => setPassword(e.target.value)}></input>
      <button onClick = {handleRegister}>Sign Up</button>
      <div className = "text-red-400">{error}</div>
    </div>
  )
}
export default Register
