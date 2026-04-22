import { useState, useEffect } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import './App.css'
import ExpenseForm from './components/ExpenseForm'
import ExpenseList from './components/ExpenseList'
import LoginForm from './components/LoginForm'
import { loginUser } from './services/auth'
import { fetchExpenses, addExpense as createExpense, deleteExpense as removeExpense, updateExpense } from './services/expenses'


function App() {
   const  [expenses, setExpenses] = useState([])
   const [token, setToken] = useState(localStorage.getItem("token"));

   async function loadExpenses(){
        try{
            const data = await fetchExpenses();
            setExpenses(data)

            }catch(err){
                  console.error("Failed to load expenses:", err.message)
                }
        }

    async function deleteExpense(expenseId){
       try{
        await removeExpense(expenseId);
        setExpenses((expenses) => expenses.filter((expense) => expense.id !== expenseId)
        );
        }catch(err){

            console.error("Failed to delete expense:", err.message);
            }
    }


   async function addExpense(expense){
        try {
             const newExpense = await createExpense(expense)
            setExpenses([...expenses, newExpense])
         } catch (err) {
        console.error("Failed to add expense:", err.message)
           }
       }
   async function  handleUpdateExpense(expense, expense_id){
       try{
           const data = await updateExpense(expense, expense_id)
           setExpenses((expenses) => expenses.map((expense) =>
           expense.id === data.id ? data : expense
           )
       );
      }catch(err){

              console.error("Failed to update expense: ", err.message)
          }
       }


    async function handleLogin(email, password){
        const data = await loginUser(email, password);
        localStorage.setItem("token", data.access_token);
        setToken(data.access_token);
        }
    function handleLogout() {
       localStorage.removeItem("token");
       setToken(null);
        setExpenses([]);
  }

        useEffect(() => {
         if (token) {
         loadExpenses();
            }
 }, [token]);
// If NOT logged in → show login page ONLY
     if (!token) {
    return <LoginForm onLogin={handleLogin} />;
  }


  // If logged in → show app
  return (
      <div>
        <h1>Expense Tracker</h1>
        <button onClick={handleLogout}>Logout</button>
        <ExpenseForm onAddExpense= {addExpense} />
         <h2> Expenses List</h2>
        <ExpenseList expenses= {expenses}
          onDeleteExpense={deleteExpense}
          onUpdateExpense= {handleUpdateExpense}
         />

      </div>

  )
}

export default App
