import { Recipe } from "../util/types";
import recipeFallbackImage from "../assets/recipe-fallback.png";
import { Link } from "@tanstack/react-router";
import { useContext } from "react";
import UserContext from "../util/userContext";
import { toggleFavourite } from "../util/favourite";

export default function RecipeCard({
  recipe,
  isFavourite,
}: {
  recipe: Recipe;
  isFavourite: boolean;
}) {
  const { user, userFavourites, setUserFavourites } = useContext(UserContext);

  return (
    <div className="card card-compact bg-base-200 grow sm:basis-1/3 md:basis-1/4 lg:basis-1/5">
      <figure>
        <img
          className="recipe-image"
          src={recipe.image ?? recipeFallbackImage}
          alt={recipe.title}
        />
      </figure>
      <div className="card-body">
        <h2 className="card-title">{recipe.title}</h2>
        {recipe.description ? (
          <p className="line-clamp-4">{recipe.description}</p>
        ) : null}
        <div className="card-actions flex">
          <Link
            to="/recipe/$recipeId"
            params={{ recipeId: `${recipe.id}` }}
            className="btn btn-primary grow"
          >
            View Recipe
          </Link>
          {user ? (
            <button
              onClick={() =>
                toggleFavourite(
                  isFavourite,
                  user,
                  recipe,
                  userFavourites,
                  setUserFavourites,
                  () => {}
                )
              }
              className="btn btn-ghost px-2"
            >
              <svg
                width="24"
                height="24"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M7 3c-1.535 0-3.078.5-4.25 1.7-2.343 2.4-2.279 6.1 0 8.5L12 23l9.25-9.8c2.279-2.4 2.343-6.1 0-8.5-2.343-2.3-6.157-2.3-8.5 0l-.75.8-.75-.8C10.078 3.5 8.536 3 7 3"
                  fill={isFavourite ? "#e74c3c" : "#000000"}
                />
              </svg>
            </button>
          ) : null}
        </div>
      </div>
    </div>
  );
}
