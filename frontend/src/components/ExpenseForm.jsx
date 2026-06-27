import {useState} from 'react'
import { CATEGORIES } from '../constants'

function ExpenseForm(props){
  const [title, setTitle] = useState("")
  const [amount, setAmount] = useState("")
  const [date, setDate] = useState("")
  const [description, setDescription] = useState("")
  const [category, setCategory] = useState("Other")
  function handleSubmit(event){
      event.preventDefault()

      if (!title.trim()) return alert("Title is required");
      if (!amount || Number(amount) <= 0) return alert("Amount must be > 0");
      if (!date) return alert("Date is required");

    const expense = {
      title: title,
      description: description,
      amount: Number(amount),
      date: date,
      category: category
    }
      props.onAddExpense(expense)
      setAmount("")
      setTitle("")
      setDescription("")
      setDate("")
      setCategory("Other")

      }

       return (
    <div>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Title</label>
          <input
            type="text"
            value={title}
            onChange={(event) => setTitle(event.target.value)}
          />
        </div>

        <div>
          <label>Amount</label>
          <input
            type="number"
            value={amount}
            onChange={(event) => setAmount(event.target.value)}
          />
        </div>

        <div>
          <label>Date</label>
          <input
            type="date"
            value={date}
            onChange={(event) => setDate(event.target.value)}
          />
        </div>

          <div>
          <label>Description</label>
          <input
            type="text"
            value={description}
            onChange={(event) => setDescription(event.target.value)}
          />
        </div>

        <div>
          <label>Category</label>
          <select
            value={category}
            onChange={(event) => setCategory(event.target.value)}
          >
            {CATEGORIES.map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
        </div>

          <div>
          <button type="submit">Add Expense</button>
        </div>
      </form>
    </div>
  )
}

export default ExpenseForm