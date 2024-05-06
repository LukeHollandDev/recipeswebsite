import { User } from "./types";

// Stringifies the user and stores in local storage.
export function setUser(user: User) {
  localStorage.setItem("user", JSON.stringify(user));
}

// Returns User object or the void if no user or invalid user is found.
export function getUser(): User | void {
  const user = localStorage.getItem("user");

  if (user) {
    const userObj = JSON.parse(user);
    if (userObj?.id && userObj?.username && userObj?.email) {
      return userObj as User;
    }
  }
}

// Stores the token in local storage.
export function setToken(token: string) {
  localStorage.setItem("token", token);
}

// Returns token or void if no token is found.
export function getToken(): string | void {
  const token = localStorage.getItem("token");

  if (token) {
    return token;
  }
}

// Clears the local storage for token and user.
export function clearTokenUser() {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
}
