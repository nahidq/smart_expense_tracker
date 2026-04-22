
import { AUTH_BASE_URL } from "./api";

 export async function loginUser(email, password){

    const response = await fetch(`${AUTH_BASE_URL}/auth/login`,{
        method: "POST",
        headers:{
            "Content-Type": "application/json",

        },
        body:JSON.stringify({ email, password }),

    });

    const data = await response.json();
    if(!response.ok){
       throw new Error(data.detail || "Login failed");
    }

    return data;
}