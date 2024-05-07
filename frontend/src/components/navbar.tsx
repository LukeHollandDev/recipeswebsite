import { Link } from "@tanstack/react-router";
import { useContext } from "react";
import UserContext from "../util/userContext";
import { logout } from "../util/authentication";

export default function Navbar({ Links }: { Links: JSX.Element[] }) {
  const { user, setUser } = useContext(UserContext);

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
          <button onClick={() => logout(setUser)} className="btn btn-ghost">
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
