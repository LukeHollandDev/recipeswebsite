import { Link, createFileRoute, redirect } from "@tanstack/react-router";
import { useContext, useEffect, useState } from "react";
import UserContext from "../util/userContext";
import Recipes from "../components/recipes";
import { Favourite, Recipe } from "../util/types";
import { isAuthenticated } from "../util/authentication";

export const Route = createFileRoute("/favourites")({
  beforeLoad: async () => {
    if (!(await isAuthenticated())) {
      throw redirect({
        to: "/",
      });
    }
  },
  component: Favourites,
});

function Favourites() {
  const { userFavourites } = useContext(UserContext);
  const [recipes, setRecipes] = useState<Recipe[]>([]);

  useEffect(() => {
    setRecipes(userFavourites.map((favourite: Favourite) => favourite.recipe));
  }, [userFavourites]);

  return (
    <>
      <div className="rounded bg-base-200 text-center p-6 mb-6">
        <div className="max-w-xl mx-auto">
          <h1 className="text-4xl font-bold">Favourite Recipes</h1>
          <p className="pt-4">
            Below is all the recipes you currently have favourited!
          </p>
        </div>
      </div>
      {userFavourites.length > 0 ? (
        <Recipes recipes={recipes} favourites={userFavourites} />
      ) : (
        <div>
          <div role="alert" className="alert">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              className="stroke-success shrink-0 w-6 h-6"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              ></path>
            </svg>
            <span>
              Looks like you've not got any recipes favourites, click the button
              below to start looking for recipes!
            </span>
          </div>
          <div className="max-w-96 m-auto">
            <Link to="/" className="btn btn-primary btn-wide btn-block mt-6">
              Discover Recipes
            </Link>
          </div>
        </div>
      )}
    </>
  );
}
