import { createRootRoute, Outlet } from "@tanstack/react-router";
import Navbar from "../components/navbar";
import { UserProvider } from "../util/userContext";

export const Route = createRootRoute({
  component: () => {
    return (
      <UserProvider>
        <Navbar />
        <hr />
        <main className="p-6 max-w-screen-xl m-auto">
          <Outlet />
        </main>
        <button
          onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
          className="sticky absolute bottom-4 right-4 btn btn-accent block max-w-max ml-auto"
        >
          Scroll to top
        </button>
      </UserProvider>
    );
  },
});
