import axios from "axios";
import { User } from "./types";
import { clearUser, getUser } from "./localstorage";

// Takes token and validates it to make sure it's valid, returns user obj if valid.
export async function authenticate(token: string): Promise<void | User> {
  return await axios
    .get(`${import.meta.env.VITE_API_URL}/users`, {
      headers: { Authorization: `Bearer ${token}` },
    })
    .then((response) => {
      // /users/ endpoint does not include the token in response
      return { ...response.data, access_token: token } as User;
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
  const token = getUser()?.access_token;
  if (token) {
    return (await authenticate(token)) ? true : false;
  }
  return false;
}

// Function which logs a user out, takes a callback which is used to update user state.
export function logout(setUserCallback: (user: null) => void) {
  // nulls user in localstorage
  clearUser();
  setUserCallback(null);
}
