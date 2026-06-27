import { useState, useEffect, useCallback } from 'react'
import './App.css'
import ExpenseForm from './components/ExpenseForm'
import ExpenseList from './components/ExpenseList'
import ExpenseFilters from './components/ExpenseFilters'
import LoginForm from './components/LoginForm'
import { loginUser } from './services/auth'
import { fetchExpenses, addExpense as createExpense, deleteExpense as removeExpense, updateExpense } from './services/expenses'

const PAGE_SIZE = 10

function App() {
  const [expenses, setExpenses] = useState([])
  const [total, setTotal] = useState(0)
  const [token, setToken] = useState(localStorage.getItem("token"))

  // Filters
  const [category, setCategory] = useState("")
  const [startDate, setStartDate] = useState("")
  const [endDate, setEndDate] = useState("")

  // Pagination
  const [offset, setOffset] = useState(0)

  // One reusable loader. useCallback keeps a stable identity that only changes
  // when a filter or the page changes — which is exactly when we want to refetch.
  const loadExpenses = useCallback(async () => {
    try {
      const data = await fetchExpenses({
        category,
        startDate,
        endDate,
        limit: PAGE_SIZE,
        offset,
      })
      setExpenses(data.items)
      setTotal(data.total)
    } catch (err) {
      console.error("Failed to load expenses:", err.message)
    }
  }, [category, startDate, endDate, offset])

  useEffect(() => {
    if (!token) return
    // Fetching data in an effect is the intended use here. The setState calls
    // happen asynchronously (after await), so the lint rule is a false positive.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    loadExpenses()
  }, [token, loadExpenses])

  // Changing a filter should send us back to the first page.
  function handleCategoryChange(value) {
    setCategory(value)
    setOffset(0)
  }
  function handleStartDateChange(value) {
    setStartDate(value)
    setOffset(0)
  }
  function handleEndDateChange(value) {
    setEndDate(value)
    setOffset(0)
  }

  async function deleteExpense(expenseId) {
    try {
      await removeExpense(expenseId)
      await loadExpenses() // refresh current page from the server
    } catch (err) {
      console.error("Failed to delete expense:", err.message)
    }
  }

  async function addExpense(expense) {
    try {
      await createExpense(expense)
      setOffset(0)        // jump to first page so the new item is visible
      await loadExpenses()
    } catch (err) {
      console.error("Failed to add expense:", err.message)
    }
  }

  async function handleUpdateExpense(expense, expense_id) {
    try {
      await updateExpense(expense, expense_id)
      await loadExpenses()
    } catch (err) {
      console.error("Failed to update expense: ", err.message)
    }
  }

  async function handleLogin(email, password) {
    const data = await loginUser(email, password)
    localStorage.setItem("token", data.access_token)
    setToken(data.access_token)
  }

  function handleLogout() {
    localStorage.removeItem("token")
    setToken(null)
    setExpenses([])
    setTotal(0)
    setOffset(0)
  }

  // If NOT logged in → show login page ONLY
  if (!token) {
    return <LoginForm onLogin={handleLogin} />
  }

  // Pagination math
  const canPrev = offset > 0
  const canNext = offset + PAGE_SIZE < total
  const currentPage = Math.floor(offset / PAGE_SIZE) + 1
  const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE))

  // If logged in → show app
  return (
    <div>
      <h1>Expense Tracker</h1>
      <button onClick={handleLogout}>Logout</button>

      <ExpenseForm onAddExpense={addExpense} />

      <h2>Expenses List</h2>

      <ExpenseFilters
        category={category}
        startDate={startDate}
        endDate={endDate}
        onCategoryChange={handleCategoryChange}
        onStartDateChange={handleStartDateChange}
        onEndDateChange={handleEndDateChange}
      />

      <ExpenseList
        expenses={expenses}
        onDeleteExpense={deleteExpense}
        onUpdateExpense={handleUpdateExpense}
      />

      <div style={{ marginTop: "10px" }}>
        <button onClick={() => setOffset(offset - PAGE_SIZE)} disabled={!canPrev}>
          Prev
        </button>
        <span style={{ margin: "0 10px" }}>
          Page {currentPage} of {totalPages} ({total} total)
        </span>
        <button onClick={() => setOffset(offset + PAGE_SIZE)} disabled={!canNext}>
          Next
        </button>
      </div>
    </div>
  )
}

export default App
