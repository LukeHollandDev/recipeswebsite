import { Link, createLazyFileRoute } from "@tanstack/react-router";
import { useContext } from "react";
import UserContext from "../util/userContext";
import Recipes from "../components/recipes";

export const Route = createLazyFileRoute("/")({
  component: Index,
});

function Index() {
  const { user } = useContext(UserContext);

  return (
    <>
      <div className="rounded bg-base-200 text-justify p-6 mb-6">
        <div className="max-w-xl mx-auto">
          <h1 className="text-4xl font-bold text-center">Hello Freshed 2</h1>
          <p className="pt-4">
            Welcome to <strong>Hello Freshed 2</strong>. This is a recipe
            website which brings together recipes from a variety of sources and
            allows see the ingredients and instructions for the recipe! With an
            account you can save recipes to your menu and favourite the ones you
            enjoyed the most!
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
      <Recipes />
    </>
  );
}
