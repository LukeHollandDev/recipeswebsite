import { Link } from "@tanstack/react-router";
import { useContext } from "react";
import UserContext from "../util/userContext";
import { logout } from "../util/authentication";

export default function Navbar() {
  const { user, setUser } = useContext(UserContext);

  return (
    <div className="navbar bg-base-100">
      <div className="navbar-start">
        <Link to="/" className="btn btn-ghost text-xl">
          Hello Freshed 2
        </Link>
      </div>

      <div className="navbar-end">
        {user ? (
          <>
            <p className="font-bold mx-2">{user.username}</p>
            <button onClick={() => logout(setUser)} className="btn btn-ghost">
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
