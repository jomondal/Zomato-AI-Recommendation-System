import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { AiSummary } from "../src/components/recommend/AiSummary";

describe("AiSummary", () => {
  it("shows placeholder when no result", () => {
    render(<AiSummary />);
    expect(screen.getByText(/Get AI Picks/i)).toBeInTheDocument();
  });

  it("shows groq summary", () => {
    render(
      <AiSummary
        result={{
          summary: "Top Italian picks in Banashankari for family dinner.",
          total_candidates: 24,
          recommendations: [],
          latency_ms: 1200,
          source: "groq",
          llm_latency_ms: 900,
        }}
      />,
    );

    expect(screen.getByText(/Top Italian picks/)).toBeInTheDocument();
  });
});
