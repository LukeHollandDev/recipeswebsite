import { createRootRoute, Link, Outlet } from "@tanstack/react-router";
import Navbar from "../components/navbar";
import { UserProvider } from "../util/userContext";

const Links = [<Link to="/">Home</Link>, <Link to="/about">About</Link>];

export const Route = createRootRoute({
  component: () => {
    return (
      <UserProvider>
        <Navbar Links={Links} />
        <hr />
        <main className="p-6 max-w-screen-xl m-auto">
          <Outlet />
        </main>
      </UserProvider>
    );
  },
});
