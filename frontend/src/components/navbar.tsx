import { Link } from "@tanstack/react-router";
import { isAuthenticated, logout } from "../util/authentication";
import { getUser } from "../util/localstorage";
import { useEffect, useState } from "react";
import { User } from "../util/types";

export default function Navbar({ Links }: { Links: JSX.Element[] }) {
  const [user, setUser] = useState<User>();

  useEffect(() => {
    async function getAuthenticatedUser() {
      if (await isAuthenticated()) {
        const tempUser = getUser();
        if (tempUser) {
          setUser(tempUser);
        }
      }
    }
    if (!user) {
      getAuthenticatedUser();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="navbar bg-base-100">
      <div className="navbar-start">
        <Link to="/" className="btn btn-ghost text-xl">
          Hello Freshed 2
        </Link>
      </div>

      <div className="navbar-center hidden lg:flex">
        <ul className="menu menu-horizontal mx-4 gap-2">
          {Links.map((Link, index) => (
            <li key={`nav-link-${index}`}>{Link}</li>
          ))}
        </ul>
      </div>

      <div className="navbar-end">
        {user ? (
          <button onClick={logout} className="btn btn-ghost">
            Logout
          </button>
        ) : (
          <Link to="/login" className="btn btn-ghost">
            Login
          </Link>
        )}
      </div>
    </div>
  );
}
