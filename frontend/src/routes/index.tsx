import { Link, createFileRoute } from "@tanstack/react-router";
import { useContext, useEffect, useState } from "react";
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
  const [searchQuery, setSearchQuery] = useState("");
  const [source, setSource] = useState("");

  const getRecipes = async (firstLoad: boolean) => {
    // build path parameters
    let pathParams = `skip=${recipes.length}&limit=24`;
    pathParams += searchQuery !== "" ? `&query=${searchQuery}` : "";
    pathParams +=
      source !== ""
        ? `&source_filter=${source.toLowerCase().replaceAll(" ", "")}`
        : "";

    axios
      .get(`${import.meta.env.VITE_API_URL}/recipes?${pathParams}`, {
        headers: { "Content-Type": "application/json" },
      })
      .then((response) => {
        if (response.status === 200) {
          let newRecipes = [];
          if (searchQuery !== "" || source !== "") {
            newRecipes = response.data;
          } else {
            newRecipes = [...recipes, ...response.data];
          }
          setRecipes(newRecipes);
          setLoadedRecipes(newRecipes);
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
  };

  const selectSource = (source: string) => {
    setSource(source);
    if (document.activeElement instanceof HTMLElement) {
      document.activeElement.blur();
    }
  };

  // initial page load to get initial recipes, only gets them if there is no loaded recipes
  useEffect(() => {
    if (getLoadedRecipes().length === 0) {
      getRecipes(true);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // useEffect for the search bar with 1 second delay
  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      getRecipes(false);
    }, 1000);

    return () => clearTimeout(delayDebounceFn);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchQuery]);

  // useEffect for the source, when source changes update the recipes
  useEffect(() => {
    getRecipes(false);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [source]);

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

      <div className="grid grid-cols-1 md:grid-cols-3 mb-6 gap-2">
        <input
          type="text"
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Recipe keyword search..."
          className="input input-bordered input-primary w-full col-span-2"
        />
        <div className="dropdown">
          <div
            tabIndex={0}
            role="button"
            className="btn w-full"
            id="source-dropdown"
          >
            Recipe source:{" "}
            <span className="italic">{source ? source : "Select Source"}</span>
          </div>
          <ul
            tabIndex={0}
            className="dropdown-content z-[1] menu p-2 shadow bg-base-100 rounded-box w-full"
          >
            <li>
              <button onClick={() => selectSource("Hello Fresh")}>
                Hello Fresh
              </button>
            </li>
            <li>
              <button onClick={() => selectSource("Just One Cookbook")}>
                Just One Cookbook
              </button>
            </li>
          </ul>
        </div>
      </div>

      {recipes.length !== 0 ? (
        <InfiniteScroll
          next={() => getRecipes(false)}
          hasMore={true}
          loader={<p>Loading more recipes...</p>}
          dataLength={recipes.length}
        >
          <Recipes recipes={recipes} favourites={userFavourites} />
        </InfiniteScroll>
      ) : (
        <p>No recipes found! Try a different search!</p>
      )}
    </>
  );
}
