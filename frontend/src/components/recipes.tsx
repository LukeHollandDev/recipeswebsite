import axios from "axios";
import { useState, useEffect } from "react";
import { Favourite, Recipe } from "../util/types";
import RecipeCard from "./recipeCard";

export default function Recipes({ favourites }: { favourites: Favourite[] }) {
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
    <div>
      <div className="flex flex-wrap gap-4">
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
