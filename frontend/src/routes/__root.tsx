import { createRootRoute, Outlet } from "@tanstack/react-router";
import Navbar from "../components/navbar";
import { UserProvider } from "../util/userContext";
import { useEffect, useRef, useState } from "react";

export const Route = createRootRoute({
  component: Index,
});

function Index() {
  const [scrollTopVisible, setScrollTopVisible] = useState(false);
  const prevScrollPos = useRef(0);

  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  useEffect(() => {
    const toggleVisibility = () => {
      const currentScrollPos = window.pageYOffset;

      // Button is displayed after scrolling for 500 pixels
      if (currentScrollPos > 500 && currentScrollPos > prevScrollPos.current) {
        setScrollTopVisible(true);
      } else {
        setScrollTopVisible(false);
      }

      prevScrollPos.current = currentScrollPos;
    };

    window.addEventListener("scroll", toggleVisibility);

    return () => window.removeEventListener("scroll", toggleVisibility);
  }, [scrollTopVisible]);

  return (
    <UserProvider>
      <Navbar />
      <hr />
      <main className="p-6 max-w-screen-xl m-auto">
        <Outlet />
      </main>
      {scrollTopVisible ? (
        <button
          onClick={scrollToTop}
          className="sticky absolute bottom-4 right-4 btn btn-accent block max-w-max ml-auto"
        >
          Scroll to top
        </button>
      ) : null}
    </UserProvider>
  );
}
