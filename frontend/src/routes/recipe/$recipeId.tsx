import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { RecipeFull } from "../../util/types";
import axios from "axios";

export const Route = createFileRoute("/recipe/$recipeId")({
  component: RecipeComponent,
});

function RecipeComponent() {
  const { recipeId } = Route.useParams();
  const [recipe, setRecipe] = useState<RecipeFull | null>(null);

  useEffect(() => {
    // make a call to the API to get the recipe details
    axios
      .get(`${import.meta.env.VITE_API_URL}/recipes/${recipeId}`, {
        headers: { "Content-Type": "application/json" },
      })
      .then((response) => {
        if (response.status === 200) {
          setRecipe(response.data);
        }
      })
      .catch((error) => {
        // TODO: handle errors properly!
        console.log(error);
      });
  }, [recipeId]);

  return <div>{recipe?.title}</div>;
}
