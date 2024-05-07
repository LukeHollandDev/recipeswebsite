import { useState, FormEvent, ChangeEvent, useContext } from "react";
import {
  createFileRoute,
  Link,
  redirect,
  useNavigate,
} from "@tanstack/react-router";
import axios from "axios";
import { User } from "../util/types";
import { isAuthenticated } from "../util/authentication";
import UserContext from "../util/userContext";

interface UserLogin {
  username: string;
  password: string;
}

export const Route = createFileRoute("/login")({
  beforeLoad: async () => {
    if (await isAuthenticated()) {
      throw redirect({
        to: "/",
      });
    }
  },
  component: () => {
    // eslint-disable-next-line react-hooks/rules-of-hooks
    const { setUser } = useContext(UserContext);
    // eslint-disable-next-line react-hooks/rules-of-hooks
    const [userLogin, setUserLogin] = useState<UserLogin>({
      username: "",
      password: "",
    });
    // eslint-disable-next-line react-hooks/rules-of-hooks
    const [error, setError] = useState("");
    // eslint-disable-next-line react-hooks/rules-of-hooks
    const navigate = useNavigate({ from: "/login" });

    const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
      setUserLogin({ ...userLogin, [event.target.name]: event.target.value });
    };

    const handleLogin = (event: FormEvent<HTMLFormElement>) => {
      event.preventDefault();
      axios
        .post(`${import.meta.env.VITE_API_URL}/users/login`, userLogin, {
          headers: { "Content-Type": "application/json" },
        })
        .then((response) => {
          if (response.status === 200) {
            setUser(response.data as User);
            navigate({ to: "/" });
          }
        })
        .catch((error) => {
          const { status, data } = error.response;
          if (status === 401) {
            setError(data.detail);
          }
        });
    };

    return (
      <div className="max-w-lg m-auto">
        <form onSubmit={handleLogin} className="card-body">
          <div className="form-control">
            <label className="label">
              <span className="label-text">Username</span>
            </label>
            <input
              name="username"
              type="text"
              placeholder="Enter your username here..."
              className="input input-bordered"
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-control">
            <label className="label">
              <span className="label-text">Password</span>
            </label>
            <input
              name="password"
              type="password"
              placeholder="Enter your password here..."
              className="input input-bordered"
              onChange={handleChange}
              required
            />
          </div>

          {error ? (
            <div role="alert" className="alert alert-error mt-3">
              <span>{error}</span>
            </div>
          ) : null}

          <div className="form-control mt-3 gap-2">
            <button className="btn btn-primary">Login</button>
          </div>
          <Link to="/" className="btn btn-base-300">
            Register
          </Link>
        </form>
      </div>
    );
  },
});
