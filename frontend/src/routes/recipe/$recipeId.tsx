import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import axios from "axios";
import { RecipeFull } from "../../util/types";
import recipeFallbackImage from "../../assets/recipe-fallback.png";

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

  return (
    <div className="rounded bg-base-200">
      <div
        className="hero rounded-tr rounded-tl"
        style={{
          backgroundImage: `url(${recipe?.image ?? recipeFallbackImage})`,
        }}
      >
        <div className="hero-overlay bg-opacity-50 rounded-tr rounded-tl"></div>
        <div className="hero-content text-center text-neutral-content">
          <div>
            <h1 className="my-5 text-5xl font-bold">{recipe?.title}</h1>
          </div>
        </div>
      </div>

      <div className="p-6">
        <p className="mb-2 font-bold">
          Recipe sourced from:{" "}
          <a href={recipe?.url} className="link link-info" target="__blank">
            {recipe?.url}
          </a>
        </p>

        {recipe?.description ? (
          <div className="mb-6">
            <h2 className="mb-2 text-3xl font-bold">Description</h2>
            <p>{recipe.description}</p>
          </div>
        ) : null}

        <div className="flex gap-2 flex-wrap mb-6">
          {recipe?.cuisine ? (
            <p className="bg-accent text-accent-content p-2 rounded">
              {recipe.cuisine}
            </p>
          ) : null}
          {recipe?.prepTime ? (
            <p className="bg-secondary text-secondary-content p-2 rounded">
              Preperation {recipe.prepTime} minutes
            </p>
          ) : null}
          {recipe?.totalTime ? (
            <p className="bg-info text-info-content p-2 rounded">
              Total time {recipe.totalTime} minutes
            </p>
          ) : null}
        </div>

        {recipe?.description ? (
          <div className="mb-6">
            <h2 className="mb-2 text-3xl font-bold">Resources</h2>
            <ul className="list-disc list-inside">
              {recipe.resources.map((resource) => (
                <li>
                  {resource.name} [
                  <a
                    href={resource.value}
                    target="__blank"
                    className="link link-info"
                  >
                    {resource.type}
                  </a>
                  ]
                </li>
              ))}
            </ul>
          </div>
        ) : null}

        <div className="mb-6">
          <h2 className="mb-2 text-3xl font-bold">Ingredients</h2>
          {recipe?.ingredient_groups.map((group) => (
            <div className="max-w-96">
              {group.name ? (
                <h3 className="mb-2 text-xl font-bold">{group.name}</h3>
              ) : null}
              <div className="grid grid-cols-12 gap-2 auto-cols-min">
                {group.ingredients.map((ingredient) => (
                  <>
                    <div className="col-span-3">
                      {ingredient.amount_lower === ingredient.amount_upper
                        ? ingredient.amount_lower
                        : `${ingredient.amount_lower}-${ingredient.amount_upper}`}{" "}
                      {ingredient.unit ? ingredient.unit : "x"}
                    </div>
                    <div className="col-span-9">
                      {ingredient.name}{" "}
                      {ingredient.note ? `${ingredient.note}` : null}
                    </div>
                  </>
                ))}
              </div>
            </div>
          ))}
          <p className="mt-2 italic">
            Some recipes might not have entirely accurate amounts, if it looks
            off verify it against the source linked above.
          </p>
        </div>

        <div>
          <h2 className="mb-2 text-3xl font-bold">Instructions</h2>
          {recipe?.instruction_groups.map((instruction_group) => (
            <div className="max-w-2xl">
              {instruction_group.name ? (
                <h3 className="mb-2 text-xl font-bold">
                  {instruction_group.name}
                </h3>
              ) : null}
              <div>
                {instruction_group.instructions.map((instruction) => (
                  <div className="mb-4">
                    <p className="font-bold bg-accent rounded p-1 inline">
                      Step {instruction.index + 1}
                    </p>
                    <p className="mt-1">{instruction.text}</p>
                    {instruction.image ? (
                      <img src={instruction.image} className="mt-2 rounded" />
                    ) : null}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
