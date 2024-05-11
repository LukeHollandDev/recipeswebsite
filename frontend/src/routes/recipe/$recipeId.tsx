import { createFileRoute } from "@tanstack/react-router";
import { useContext, useEffect, useState } from "react";
import axios from "axios";
import { Favourite, Instruction, RecipeFull } from "../../util/types";
import recipeFallbackImage from "../../assets/recipe-fallback.png";
import UserContext from "../../util/userContext";
import { toggleFavourite } from "../../util/favourite";

export const Route = createFileRoute("/recipe/$recipeId")({
  component: RecipeComponent,
});

function RecipeComponent() {
  const { user, userFavourites, setUserFavourites } = useContext(UserContext);
  const { recipeId } = Route.useParams();
  const [recipe, setRecipe] = useState<RecipeFull | null>(null);
  const [isFavourite, setIsFavourite] = useState(false);

  useEffect(() => {
    // make a call to the API to get the recipe details
    axios
      .get(`${import.meta.env.VITE_API_URL}/recipes/${recipeId}`, {
        headers: { "Content-Type": "application/json" },
      })
      .then((response) => {
        if (response.status === 200) {
          setRecipe(response.data);
          if (user) {
            setIsFavourite(
              !!userFavourites.find(
                (favourite: Favourite) =>
                  favourite.recipe_id === response.data.id
              )
            );
          }
        }
      })
      .catch((error) => {
        // TODO: handle errors properly!
        console.log(error);
      });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [recipeId, userFavourites]);

  return (
    <div className="rounded bg-base-200">
      <div
        className="hero rounded-tr rounded-tl"
        style={{
          backgroundImage: `url(${recipe?.image ?? recipeFallbackImage})`,
        }}
      >
        <div className="hero-overlay bg-opacity-50 rounded-tr rounded-tl"></div>
        <div className="hero-content text-center text-base-100">
          <div>
            <h1 className="my-5 text-5xl font-bold">{recipe?.title}</h1>
            {user ? (
              <p className="flex items-center gap-1 mb-2">
                <button
                  onClick={() =>
                    toggleFavourite(
                      isFavourite,
                      user,
                      recipe,
                      userFavourites,
                      setUserFavourites,
                      setIsFavourite
                    )
                  }
                  className="btn btn-sm m-auto"
                >
                  {isFavourite
                    ? "Remove recipe from your favourites"
                    : "Add recipe to your favourites"}
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
              </p>
            ) : null}
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

        {recipe?.resources?.length && recipe.resources.length > 0 ? (
          <div className="mb-6">
            <h2 className="mb-2 text-3xl font-bold">Resources</h2>
            <ul className="list-disc list-inside">
              {recipe.resources.map((resource) => (
                <li key={resource.id}>
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
            <div key={group.id} className="max-w-96">
              {group.name ? (
                <h3 className="mb-2 text-xl font-bold">{group.name}</h3>
              ) : null}
              {group.ingredients.map((ingredient) => (
                <div
                  key={ingredient.id}
                  className="grid grid-cols-12 mb-1 auto-cols-min"
                >
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
                </div>
              ))}
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
            <div key={instruction_group.id} className="max-w-2xl">
              {instruction_group.name ? (
                <h3 className="mb-2 text-xl font-bold">
                  {instruction_group.name}
                </h3>
              ) : null}
              <div>
                {instruction_group.instructions
                  .sort((a: Instruction, b: Instruction) => a.index - b.index)
                  .map((instruction) => (
                    <div key={instruction.id} className="mb-4">
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
