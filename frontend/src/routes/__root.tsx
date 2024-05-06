import { createRootRoute, Link, Outlet } from "@tanstack/react-router";
import Navbar from "../components/navbar";
import { AuthContext } from "../context/AuthContext";
import { useAuth } from "../hooks/useAuth";

const Links = [<Link to="/">Home</Link>, <Link to="/about">About</Link>];

export const Route = createRootRoute({
  component: () => {
    // eslint-disable-next-line react-hooks/rules-of-hooks
    const { user, setUser } = useAuth();
    return (
      <AuthContext.Provider value={{ user, setUser }}>
        <Navbar Links={Links} />
        <hr />
        <main className="p-6 max-w-screen-xl m-auto">
          <Outlet />
        </main>
      </AuthContext.Provider>
    );
  },
});
