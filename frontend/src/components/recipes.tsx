import { Favourite, Recipe } from "../util/types";
import RecipeCard from "./recipeCard";

export default function Recipes({
  recipes,
  favourites,
}: {
  recipes: Recipe[];
  favourites: Favourite[];
}) {
  return (
    <div>
      <div className="grid sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {recipes.map((recipe: Recipe) => (
          <RecipeCard
            key={recipe.id}
            recipe={recipe}
            isFavourite={
              !!favourites.find(
                (favourite: Favourite) => favourite.recipe_id === recipe.id
              )
            }
          />
        ))}
      </div>
    </div>
  );
}
