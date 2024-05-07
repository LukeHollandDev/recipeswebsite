import { Recipe } from "../util/types";
import recipeFallbackImage from "../assets/recipe-fallback.png";
import { Link } from "@tanstack/react-router";

export default function RecipeCard({ recipe }: { recipe: Recipe }) {
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
        </div>
      </div>
    </div>
  );
}
