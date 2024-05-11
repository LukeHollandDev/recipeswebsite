import { Link, createFileRoute } from "@tanstack/react-router";
import { useCallback, useContext, useEffect, useState } from "react";
import axios from "axios";
import InfiniteScroll from "react-infinite-scroll-component";
import UserContext from "../util/userContext";
import Recipes from "../components/recipes";
import { Recipe } from "../util/types";
import { getLoadedRecipes, setLoadedRecipes } from "../util/localstorage";

export const Route = createFileRoute("/")({
  component: Index,
  onStay: () => {
    sessionStorage.removeItem("scrollPosition");
  },
  onLeave: () => {
    sessionStorage.setItem("scrollPosition", JSON.stringify(window.scrollY));
  },
});

function Index() {
  const { user, userFavourites } = useContext(UserContext);
  const [recipes, setRecipes] = useState<Recipe[]>(getLoadedRecipes());

  const getRecipes = useCallback(
    async (firstLoad: boolean) => {
      axios
        .get(
          `${import.meta.env.VITE_API_URL}/recipes?skip=${recipes.length}&limit=24`,
          {
            headers: { "Content-Type": "application/json" },
          }
        )
        .then((response) => {
          if (response.status === 200) {
            setRecipes([...recipes, ...response.data]);
            setLoadedRecipes([...recipes, ...response.data]);
            if (firstLoad) {
              // set scroll position
              if (sessionStorage.getItem("scrollPosition")) {
                window.scrollTo({
                  top: JSON.parse(
                    sessionStorage.getItem("scrollPosition") ?? "0"
                  ),
                  behavior: "smooth",
                });
              }
            }
          }
        })
        .catch((error) => {
          // TODO: handle errors properly!
          console.log(error);
        });
    },
    [recipes]
  );

  useEffect(() => {
    if (getLoadedRecipes().length === 0) {
      getRecipes(true);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <>
      <div className="rounded bg-base-200 text-center p-6 mb-6">
        <div className="max-w-xl mx-auto">
          <h1 className="text-4xl font-bold">Recipe Website</h1>
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

      <InfiniteScroll
        next={() => getRecipes(false)}
        hasMore={true}
        loader={<p>Loading more recipes...</p>}
        dataLength={recipes.length}
      >
        <Recipes recipes={recipes} favourites={userFavourites} />
      </InfiniteScroll>
    </>
  );
}
