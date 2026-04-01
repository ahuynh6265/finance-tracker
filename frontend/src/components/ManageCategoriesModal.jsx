import {useState} from "react"
import {createCategory, updateCategory} from "../api/api"

function ManageCategoriesModal({categories, onDeleteCategory, onCategoryChanged, onClose}) {
  const [name, setName] = useState("")
  const [newName, setNewName] = useState("")
  const [editCategoryID, setEditCategoryID] = useState("")
  const [showCreateCategories, setShowCreateCategories] = useState(false)

  function handleCreateCategory() {
    createCategory({name: name}).then(() => {
      onCategoryChanged()
      setName("")
      setShowCreateCategories(false)
    }).catch(err => console.error(err))
  }

  function handleUpdateCategory(category_id) {
    updateCategory(category_id, {name: newName}).then(() => {
      onCategoryChanged()
      setEditCategoryID("")
      setNewName("")
    }).catch(err => console.error(err))
  }

  return (
  <div className = "modal-overlay">
    <div className = "modal-content">
      <h1 className = "absolute top-4 left-4 text-gray-300 text-xl font-semibold">Manage Categories</h1>
      <button className = "absolute top-4 right-4 text-white font-semibold" onClick = {onClose}>Close</button>
      <table>
        <tbody>
          {categories.map(category =>
            <tr key = {category.id}> 
              {(editCategoryID === category.id) ? (
                <>
                  <td><input value = {newName} onChange = {(e) => setNewName(e.target.value)}></input></td>
                  <td><button onClick = {() => handleUpdateCategory(category.id)}>Save Category</button></td>
                </>
              ): (
                <>
                <td>{category.name}</td>
                    <td>
                      <button className = "mr-2" onClick = {() => onDeleteCategory(category.id)}>Delete</button>
                      <button onClick = {() => {setEditCategoryID(category.id); setNewName(category.name)}}>Edit</button>
                    </td>
                  </>
              )}
            </tr>
          )}
        </tbody>
      </table>
      <button onClick = {(e) => setShowCreateCategories(true)}>Create</button> 
      {(showCreateCategories) ? (
        <div className = "-mt-4">
          <input className = "w-full" placeholder = "Enter Category Name" value = {name} onChange = {(e) => setName(e.target.value)}></input>
          <div className = "flex justify-around p-6">
            <button className = "text-gray-300 text-l font-semibold" onClick = {handleCreateCategory}>Create Category</button>
            <button className = "text-gray-300 text-l font-semibold" onClick = {(e) => setShowCreateCategories(false)}>Discard</button>
          </div>
        </div>
      ): null}  
    </div>
  </div> 
  )
}
export default ManageCategoriesModal