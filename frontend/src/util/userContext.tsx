import {
  Dispatch,
  SetStateAction,
  createContext,
  useEffect,
  useState,
} from "react";
import { ReactNode } from "@tanstack/react-router";

import { Favourite, User } from "./types";
import {
  setUser as setUserLocalStorage,
  getUser as getUserLocalStorage,
} from "../util/localstorage";
import axios from "axios";

const UserContext = createContext<{
  user: User | null;
  setUser: Dispatch<SetStateAction<User | null>>;
  userFavourites: Favourite[];
  setUserFavourites: Dispatch<SetStateAction<Favourite[]>>;
}>({
  user: null,
  setUser: () => {},
  userFavourites: [],
  setUserFavourites: () => {},
});

export const UserProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [userFavourites, setUserFavourites] = useState<Favourite[]>([]);

  useEffect(() => {
    if (!user && getUserLocalStorage()) {
      setUser(getUserLocalStorage());
    }
    setUserLocalStorage(user);
  }, [user]);

  // use effect to get user favourites, depends on user
  useEffect(() => {
    if (user && user.access_token) {
      // make axios request to get the user's favourites
      axios
        .get(`${import.meta.env.VITE_API_URL}/users/favourites`, {
          headers: { Authorization: `Bearer ${user.access_token}` },
        })
        .then((response) => {
          setUserFavourites(response.data);
        })
        .catch((error) => {
          const { status, data } = error.response;
          if (status !== 401) {
            console.error(data.detail);
          }
        });
    } else {
      setUserFavourites([]);
    }
  }, [user]);

  return (
    <UserContext.Provider
      value={{
        user,
        setUser,
        userFavourites,
        setUserFavourites,
      }}
    >
      {children}
    </UserContext.Provider>
  );
};

export default UserContext;
