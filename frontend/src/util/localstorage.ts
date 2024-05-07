import { User } from "./types";

// Stringifies the user and stores in local storage.
export function setUser(user: User | null) {
  localStorage.setItem("user", JSON.stringify(user));
}

// Returns User object or the void if no user or invalid user is found.
export function getUser(): User | null {
  const user = localStorage.getItem("user");

  if (user) {
    const userObj = JSON.parse(user);
    if (userObj?.id && userObj?.username && userObj?.email) {
      return userObj as User;
    }
  }

  return null;
}

// Clears the local storage user.
export function clearUser() {
  localStorage.removeItem("user");
}
