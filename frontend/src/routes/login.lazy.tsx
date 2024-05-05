import { createLazyFileRoute } from "@tanstack/react-router";

export const Route = createLazyFileRoute("/login")({
  component: () => (
    <div className="max-w-lg m-auto">Login page will go here!</div>
  ),
});
