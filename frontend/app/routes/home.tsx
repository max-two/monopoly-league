import client from "api/client";
import type { Route } from "./+types/home";
import { useEffect, useState } from "react";
import type { components } from "api/schema";
import { Button } from "@radix-ui/themes";
export function meta({}: Route.MetaArgs) {
  return [
    { title: "New React Router App" },
    { name: "description", content: "Welcome to React Router!" },
  ];
}

export default function Home() {
  const [games, setGames] = useState<components["schemas"]["Game"][]>([]);

  useEffect(() => {
    const fetchData = async () => {
      const { data } = await client.GET("/games");
      if (data) {
        setGames(data);
      }
    };
    fetchData();
  }, []);

  const click = async () => {
    const { data } = await client.POST("/games", {
      body: {
        id: 123,
        week: 5,
        home_team: "Team A",
        away_team: "Team B",
      },
    });
  };

  return (
    <div>
      <h1>Games</h1>
      <Button onClick={click}>Add Game</Button>
      <ul>
      {games.map((game) => (
          <li key={game.id}>
            {game.home_team} vs {game.away_team}
          </li>
        ))}
      </ul>
    </div>
  );
}
