import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { RecommendationCard } from "../src/components/recommend/RecommendationCard";

const sampleItem = {
  rank: 1,
  restaurant_id: 42,
  name: "Onesta",
  rating: 4.6,
  votes: 2556,
  cost_for_two: 600,
  location: "Banashankari",
  city: "Banashankari",
  cuisines: "Pizza, Cafe, Italian",
  match_score: 96,
  reason: "Highest rated Italian cafe with great pizza reviews.",
  highlights: ["4.6★", "₹600 for two"],
  url: "https://www.zomato.com/bangalore/onesta",
  online_order: true,
  book_table: true,
};

describe("RecommendationCard", () => {
  it("displays restaurant details and match score", () => {
    render(<RecommendationCard item={sampleItem} />);

    expect(screen.getByText("Onesta")).toBeInTheDocument();
    expect(screen.getByText("4.6")).toBeInTheDocument();
    expect(screen.getByText(/Highest rated Italian cafe/)).toBeInTheDocument();
    expect(screen.getByText("96% match")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /View on Zomato/i })).toBeInTheDocument();
  });
});
