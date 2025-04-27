import client from "api/client";
import type { Route } from "./+types/home";
import { useEffect } from "react";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "New React Router App" },
    { name: "description", content: "Welcome to React Router!" },
  ];
}

export default function Home() {
  useEffect(() => {
    const fetchData = async () => {
      const { data, error } = await client.GET("/");
      console.log(data);
    };
    fetchData();
  }, []);

  return <div>Hello</div>;
}
