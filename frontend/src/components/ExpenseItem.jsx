import { useState, useEffect } from 'react'

function ExpenseItem({ expense, onDeleteExpense, onUpdateExpense}) {

  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(expense.title);
  const [description, setDescription] = useState(expense.description);
  const [amount, setAmount] = useState(expense.amount);
  const [date, setDate] = useState(expense.date);

     function handleSave() {
       const updatedExpense = {
      title: title,
      description: description,
      amount: Number(amount),
      date: date,
    };
    console.log("updatedExpense:", updatedExpense);

    onUpdateExpense(updatedExpense,expense.id);
    setIsEditing(false);
  }

if (isEditing) {
    return (
      <div style={{ border: "1px solid gray", margin: "10px", padding: "10px" }}>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />

        <input
          type="text"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />

        <input
          type="number"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
        />

        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
        />

        <button onClick={handleSave}>Save</button>
        <button onClick={() => setIsEditing(false)}>Cancel</button>
      </div>
    );
  }



  return (

    <div  style={{ border: "1px solid gray", margin: "10px", padding: "10px" }}>

      <p> <strong>Title:</strong>{expense.title}</p>
      <p> <strong>Description:</strong>{expense.description}</p>
      <p><strong>Amount:</strong> {expense.amount}</p>
      <p><strong>Date:</strong> {expense.date}</p>
     <button
         onClick={() => {
            if (window.confirm("Delete this expense?")) {
                onDeleteExpense(expense.id);
    }
  }}
>
  Delete
</button>
       <button onClick={() => setIsEditing(true)}>
         Edit
      </button>
    </div>
  );
}
export default ExpenseItem