import {useState} from "react"
import {userRegister} from "../api/api"
import {useNavigate} from "react-router-dom"

function Register() {
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const navigate = useNavigate()

  function handleRegister() {
    userRegister({name: name, email: email, password: password}).then(response => {
      navigate("/login")
    }).catch(err => console.error(err))
  }

  return (
    <div>
      <input value = {name} placeholder = "Name" onChange = {(e) => setName(e.target.value)}></input>
      <input value = {email} placeholder = "Email" onChange = {(e) => setEmail(e.target.value)}></input>
      <input type = "password" value = {password} placeholder = "Password" onChange = {(e) => setPassword(e.target.value)}></input>
      <button onClick = {handleRegister}>Sign Up</button>
    </div>
  )
}
export default Register
