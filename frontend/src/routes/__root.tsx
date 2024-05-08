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
      </UserProvider>
    );
  },
});
