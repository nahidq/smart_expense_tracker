import { CATEGORIES } from '../constants'

function ExpenseFilters({
  category,
  startDate,
  endDate,
  onCategoryChange,
  onStartDateChange,
  onEndDateChange,
}) {
  return (
    <div style={{ margin: "10px 0" }}>
      <label>Category </label>
      <select value={category} onChange={(e) => onCategoryChange(e.target.value)}>
        <option value="">All</option>
        {CATEGORIES.map((c) => (
          <option key={c} value={c}>{c}</option>
        ))}
      </select>

      <label> From </label>
      <input
        type="date"
        value={startDate}
        onChange={(e) => onStartDateChange(e.target.value)}
      />

      <label> To </label>
      <input
        type="date"
        value={endDate}
        onChange={(e) => onEndDateChange(e.target.value)}
      />
    </div>
  )
}

export default ExpenseFilters
