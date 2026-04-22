import { EXPENSE_BASE_URL, getToken } from "./api";

export async function fetchExpenses() {
  const response = await fetch(`${EXPENSE_BASE_URL}/expenses/`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${getToken()}`,
    },
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to fetch expenses");
  }

  return data;
}



export async function addExpense(expense){

 const response = await fetch(`${EXPENSE_BASE_URL}/expenses/`, {
        method: "POST",
        headers:{
          "Content-Type": "application/json",
          Authorization: `Bearer ${getToken()}`,
        },
         body: JSON.stringify(expense),
 });

 const data = await response.json();

 if (!response.ok){

    throw new Error(data.detail || "Failed to add an expense")

 }
 return data
}


export async function deleteExpense(expenseId){

 const response = await fetch(`${EXPENSE_BASE_URL}/expenses/${expenseId}`,{
        method: "DELETE",
        headers: {

                    Authorization: `Bearer ${getToken()}`,

                  },
 });


   if(!response.ok){
       const data = await response.json();
      throw new Error(data.detail || "Failed to add expenses");
   }

   return true
}

export async function updateExpense(expense, expense_id){

    console.log("expense sent to updateExpense:", expense);

   const response = await fetch(`${EXPENSE_BASE_URL}/expenses/${expense_id}`,
    {
     method: "PATCH",
    headers: {

      "Content-Type": "application/json",
      Authorization: ` Bearer ${getToken()}`,
        },
   body: JSON.stringify(expense),

   });

   const data = await response.json();

   if (!response.ok){
     throw new Error(data.detail || "Failed to update the expense")

   }

 return data


}