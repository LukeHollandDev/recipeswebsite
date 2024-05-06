import axios from "axios";
import { User } from "./types";
import { clearTokenUser, getToken, setToken, setUser } from "./localstorage";

// Takes token and validates it to make sure it's valid, returns user obj if valid.
export async function authenticate(token: string): Promise<void | User> {
  return await axios
    .get(`${import.meta.env.VITE_API_URL}/users`, {
      headers: { Authorization: `Bearer ${token}` },
    })
    .then((response) => {
      return response.data as User;
    })
    .catch((error) => {
      const { status, data } = error.response;
      // Allow it to silently fail, as void will be returned on unauthorised.
      if (status !== 401) {
        console.error(data.detail);
      }
    });
}

// Helper function which gets token and uses it to try and authenticate.
export async function isAuthenticated(): Promise<boolean> {
  const token = getToken();
  if (token) {
    return (await authenticate(token)) ? true : false;
  }
  return false;
}

// "Logs in" a user by setting user and token local storage.
export async function login(user: User, token: string) {
  setUser(user);
  setToken(token);
  window.location.reload();
}

// "Logs out" a user by removing the token and user local storage.
export async function logout() {
  clearTokenUser();
  window.location.reload();
}
