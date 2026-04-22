

export const AUTH_BASE_URL = "http://127.0.0.1:8000";
export const EXPENSE_BASE_URL = "http://127.0.0.1:8001";

export function getToken() {
  return localStorage.getItem("token");
}