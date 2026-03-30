import {useState, useEffect} from "react"
import {getCategories, createCategory, deleteCategory, updateCategory} from "../api/api"

function Categories() {
  const [categories, setCategories] = useState(null)
  const [name, setName] = useState("")

  const [current_id, setID] = useState(null)
  const [newName, setNewName] = useState ("")

  useEffect (() => {
    getCategories().then(response => {
      setCategories(response.data)
    })
  }, [])

  function handleCreate() {
    createCategory({name: name}).then(() => getCategories().then(response => {
      setCategories(response.data)
      setName("")
    }))  
  }

  function handleDelete(category_id) {
    deleteCategory(category_id).then(() => getCategories().then(response => {
      setCategories(response.data)
    }))
  }

  function handleUpdate(category_id) {
    updateCategory(category_id, {name: newName}).then(() => getCategories().then(response => {
      setCategories(response.data)
      setID(null)
      setNewName("")
    }))
  }

  function renderCategory(category) {
    return <div key = {category.id}>
      {(current_id === category.id) 
      ? (
      <div> 
        <input value = {newName} onChange = {(e) => setNewName(e.target.value)}></input>
        <button onClick = {() => handleUpdate(category.id)}>Save</button> 
      </div>
      )
      : (
        <div>
          <div>{category.name}</div>
          <button onClick = {() => handleDelete(category.id)}>Delete Category</button>
          <button onClick = {() => {setID(category.id); setNewName(category.name)}}>Edit</button>
        </div> 
      )
    }
    </div>
  }

  if (!categories) return <div>Loading...</div> 
  else return (
    <div>
      <input placeholder = "Enter Category Name" value = {name} onChange = {(e) => setName(e.target.value)}></input>
      <button onClick = {handleCreate}>Create Category</button>
      {categories.map(category => renderCategory(category))}
    </div> 
  )
}

export default Categories 