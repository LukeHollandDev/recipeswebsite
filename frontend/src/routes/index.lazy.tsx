import { Link, createLazyFileRoute } from "@tanstack/react-router";
import { useContext, useEffect, useState } from "react";
import UserContext from "../util/userContext";
import Recipes from "../components/recipes";
import axios from "axios";
import { Recipe } from "../util/types";

export const Route = createLazyFileRoute("/")({
  component: Index,
});

function Index() {
  const { user, userFavourites } = useContext(UserContext);
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [skip] = useState(0);

  useEffect(() => {
    // get recipes from api using skip param
    axios
      .get(`${import.meta.env.VITE_API_URL}/recipes?skip=${skip}&limit=24`, {
        headers: { "Content-Type": "application/json" },
      })
      .then((response) => {
        if (response.status === 200) {
          setRecipes([...recipes, ...response.data]);
        }
      })
      .catch((error) => {
        // TODO: handle errors properly!
        console.log(error);
      });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [skip]);

  return (
    <>
      <div className="rounded bg-base-200 text-center p-6 mb-6">
        <div className="max-w-xl mx-auto">
          <h1 className="text-4xl font-bold">Hello Freshed 2</h1>
          <p className="pt-4">
            A website which brings together recipes from a variety of sources!
          </p>
          {!user ? (
            <div className="flex gap-2 mt-4 flex-wrap">
              <Link to="/register" className="btn btn-primary grow">
                Create an account!
              </Link>
              <Link to="/login" className="btn btn-secondary grow">
                Login to your account!
              </Link>
            </div>
          ) : null}
        </div>
      </div>
      <Recipes recipes={recipes} favourites={userFavourites} />
    </>
  );
}
