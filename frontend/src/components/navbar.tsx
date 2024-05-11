import { Link } from "@tanstack/react-router";
import { useContext } from "react";
import UserContext from "../util/userContext";
import { logout } from "../util/authentication";

export default function Navbar() {
  const { user, setUser } = useContext(UserContext);

  return (
    <div className="navbar bg-base-100 sticky top-0 z-50">
      <div className="navbar-start">
        <Link to="/" className="btn btn-ghost text-xl">
          Recipe Website
        </Link>
      </div>

      <div className="navbar-end">
        {user ? (
          <>
            <Link
              to="/favourites"
              className="btn btn-sm btn-primary font-bold mx-2"
            >
              {user.username}
            </Link>
            <button
              onClick={() => logout(setUser)}
              className="btn btn-sm btn-ghost"
            >
              Logout
            </button>
          </>
        ) : (
          <Link to="/login" className="btn btn-ghost">
            Login
          </Link>
        )}
      </div>
    </div>
  );
}
