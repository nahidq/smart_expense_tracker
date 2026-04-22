import {useState} from 'react'
import ExpenseItem from './ExpenseItem'

function ExpenseList(props){

    return (
    <div>
      {
          props.expenses.map((expense) => (
        <ExpenseItem
           key={expense.id}
           expense={expense}
            onDeleteExpense={props.onDeleteExpense}
            onUpdateExpense = {props.onUpdateExpense}
           />
      )
  )
  }
    </div>
  )
    }
export default ExpenseList