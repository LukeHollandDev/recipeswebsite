import { createLazyFileRoute } from "@tanstack/react-router";
import { useContext } from "react";
import UserContext from "../util/userContext";

export const Route = createLazyFileRoute("/")({
  component: Index,
});

function Index() {
  const { user } = useContext(UserContext);

  return (
    <>
      <div className="rounded bg-base-200 text-justify py-6 mb-6">
        <div className="max-w-xl mx-auto">
          <h1 className="text-4xl font-bold text-center">Hello Freshed 2</h1>
          <p className="py-4">
            Welcome to <strong>Hello Freshed 2</strong>. This is a recipe
            website which brings together recipes from a variety of sources and
            allows you to save them to the your account. You can favourite
            recipes and build a menu of recipes you want to cook for the week!
          </p>
          <div className="flex gap-2">
            <button className="btn btn-primary grow">
              Have an account? Login!
            </button>
            <button className="btn btn-secondary grow">
              Create a new account!
            </button>
          </div>
        </div>
      </div>
      Hello {user?.username}
    </>
  );
}
