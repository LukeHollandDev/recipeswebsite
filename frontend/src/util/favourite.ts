import axios from "axios";
import { Favourite, Recipe, User } from "./types";
import { Dispatch, SetStateAction } from "react";

export function toggleFavourite(
  isFavourite: boolean,
  user: User | null,
  recipe: Recipe | null,
  userFavourites: Favourite[],
  setUserFavourites: Dispatch<SetStateAction<Favourite[]>>,
  setIsFavourite: Dispatch<SetStateAction<boolean>>
) {
  if (!recipe) {
    return;
  }

  if (isFavourite) {
    axios
      .delete(`${import.meta.env.VITE_API_URL}/users/favourite/${recipe.id}`, {
        headers: { Authorization: `Bearer ${user?.access_token}` },
      })
      .then(() => {
        let index = -1;
        for (let i = 0; i < userFavourites.length; i++) {
          if (userFavourites[i].recipe_id === recipe.id) {
            index = i;
            break;
          }
        }
        if (index !== -1) {
          userFavourites.splice(index, 1);
          setUserFavourites([...userFavourites]);
          setIsFavourite(false);
        }
      })
      .catch((error) => {
        const { status, data } = error.response;
        if (status !== 401) {
          console.error(data.detail);
        }
      });
  } else {
    axios(`${import.meta.env.VITE_API_URL}/users/favourite/${recipe.id}`, {
      method: "post",
      headers: { Authorization: `Bearer ${user?.access_token}` },
    })
      .then((response) => {
        setUserFavourites([...userFavourites, response.data]);
        setIsFavourite(true);
      })
      .catch((error) => {
        const { status, data } = error.response;
        if (status !== 401) {
          console.error(data.detail);
        }
      });
  }
}
