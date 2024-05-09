import {
  Link,
  createFileRoute,
  redirect,
  useNavigate,
} from "@tanstack/react-router";
import { isAuthenticated } from "../util/authentication";
import { ChangeEvent, FormEvent, useContext, useState } from "react";
import UserContext from "../util/userContext";
import axios from "axios";
import { User } from "../util/types";

interface UserRegister {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
}

export const Route = createFileRoute("/register")({
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
    const [userRegister, setUserRegister] = useState<UserRegister>({
      username: "",
      email: "",
      password: "",
      password_confirm: "",
    });
    // eslint-disable-next-line react-hooks/rules-of-hooks
    const [error, setError] = useState("");
    // eslint-disable-next-line react-hooks/rules-of-hooks
    const navigate = useNavigate({ from: "/login" });

    const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
      setUserRegister({
        ...userRegister,
        [event.target.name]: event.target.value,
      });
    };

    const handleRegister = (event: FormEvent<HTMLFormElement>) => {
      event.preventDefault();
      // passwords both match
      if (userRegister.password !== userRegister.password_confirm) {
        setError("Passwords do not match, please ensure they match.");
        return;
      }
      axios
        .post(`${import.meta.env.VITE_API_URL}/users/register`, userRegister, {
          headers: { "Content-Type": "application/json" },
        })
        .then((response) => {
          if (response.status === 200) {
            setUser(response.data as User);
            navigate({ to: "/" });
          }
        })
        .catch((error) => {
          const { data } = error.response;
          setError(data.detail);
        });
    };

    return (
      <div className="max-w-lg m-auto">
        <h1 className="text-2xl font-bold text-center">
          Create a Recipe Website account!
        </h1>
        <form onSubmit={handleRegister} className="card-body">
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
              <span className="label-text">Email</span>
            </label>
            <input
              name="email"
              type="email"
              placeholder="Enter your email here..."
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

          <div className="form-control">
            <input
              name="password_confirm"
              type="password"
              placeholder="Confirm your password here..."
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
            <button className="btn btn-primary">Create Account</button>
          </div>
          <Link to="/login" className="btn btn-base-300">
            Already have an account? Login!
          </Link>
        </form>
      </div>
    );
  },
});
