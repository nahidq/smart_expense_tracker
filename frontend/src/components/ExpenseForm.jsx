import {useState} from 'react'

function ExpenseForm(props){
  const [title, setTitle] = useState("")
  const [amount, setAmount] = useState("")
  const [date, setDate] = useState("")
  const [description, setDescription] = useState("")
  function handleSubmit(event){
      event.preventDefault()

      if (!title.trim()) return alert("Title is required");
      if (!amount || Number(amount) <= 0) return alert("Amount must be > 0");
      if (!date) return alert("Date is required");

    const expense = {
      title: title,
      description: description,
      amount: Number(amount),
      date: date
    }
      props.onAddExpense(expense)
      console.log(expense)
      setAmount("")
      setTitle("")
      setDescription("")
      setDate("")

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

{/*         <div> */}
{/*           <label>Category</label> */}
{/*           <select */}
{/*             value={Category} */}
{/*             onChange={(event) => setCategory(event.target.value)} */}
{/*           > */}
{/*             <option value="">Select description</option> */}
{/*             <option value="Food">Food</option> */}
{/*             <option value="Transport">Transport</option> */}
{/*             <option value="Shopping">Shopping</option> */}
{/*           </select> */}
{/*         </div> */}

          <div>
          <button type="submit">Add Expense</button>
        </div>
      </form>
    </div>
  )
}

export default ExpenseForm