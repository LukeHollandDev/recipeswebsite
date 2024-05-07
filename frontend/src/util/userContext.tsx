import {
  Dispatch,
  SetStateAction,
  createContext,
  useEffect,
  useState,
} from "react";
import { ReactNode } from "@tanstack/react-router";

import { User } from "./types";
import {
  setUser as setUserLocalStorage,
  getUser as getUserLocalStorage,
} from "../util/localstorage";

const UserContext = createContext<{
  user: User | null;
  setUser: Dispatch<SetStateAction<User | null>>;
}>({ user: null, setUser: () => {} });

export const UserProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    if (!user && getUserLocalStorage()) {
      setUser(getUserLocalStorage());
    }
    setUserLocalStorage(user);
  }, [user]);

  return (
    <UserContext.Provider value={{ user, setUser }}>
      {children}
    </UserContext.Provider>
  );
};

export default UserContext;
