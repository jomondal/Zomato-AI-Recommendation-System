import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { KpiCards } from "../src/components/dashboard/KpiCards";

describe("KpiCards", () => {
  it("renders overview metrics from stats", () => {
    render(
      <KpiCards
        stats={{
          total_restaurants: 480,
          average_rating: 3.7,
          average_cost_for_two: 555.43,
          total_cities: 1,
        }}
      />,
    );

    expect(screen.getByText("Matching Restaurants")).toBeInTheDocument();
    expect(screen.getByText("480")).toBeInTheDocument();
    expect(screen.getByText("3.7")).toBeInTheDocument();
    expect(screen.getByText("1")).toBeInTheDocument();
  });
});
