import type { Route } from "./+types/home";
import { Welcome } from "../welcome/welcome";
import { Button } from "@mantine/core";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "New React Router App" },
    { name: "description", content: "Welcome to React Router!" },
  ];
}

export default function Home() {
  return (
    <div>
      <Button>Click</Button>
    </div>
  );
}
