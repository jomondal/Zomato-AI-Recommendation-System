import { afterEach, describe, expect, it, vi } from "vitest";

import { getOverviewStats, postRecommend, toRecommendRequest } from "../src/services/api";

describe("api service", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("toRecommendRequest maps form values to API payload", () => {
    const payload = toRecommendRequest({
      city: "Banashankari",
      location: "",
      cuisines: ["Italian", "Pizza"],
      minRating: 4.0,
      maxPrice: 700,
      freeText: "good pizza",
    });

    expect(payload).toEqual({
      city: "Banashankari",
      min_rating: 4.0,
      max_price: 700,
      cuisines: ["Italian", "Pizza"],
      free_text: "good pizza",
      use_llm: true,
      limit: 5,
    });
  });

  it("getOverviewStats fetches overview data", async () => {
    const mockStats = {
      total_restaurants: 51717,
      restaurants_with_rating: 41665,
      average_rating: 3.7,
      average_cost_for_two: 555.43,
      total_cities: 30,
      total_cuisines: 107,
    };

    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: async () => mockStats,
      }),
    );

    const result = await getOverviewStats();
    expect(result.total_restaurants).toBe(51717);
    expect(fetch).toHaveBeenCalledWith("/api/v1/stats/overview", expect.any(Object));
  });

  it("postRecommend sends recommend request", async () => {
    const mockResponse = {
      summary: "Great picks",
      total_candidates: 1,
      recommendations: [],
      latency_ms: 100,
      source: "groq",
      llm_latency_ms: 80,
    };

    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: async () => mockResponse,
      }),
    );

    const result = await postRecommend({ city: "Banashankari", limit: 3 });
    expect(result.source).toBe("groq");
    expect(fetch).toHaveBeenCalledWith(
      "/api/v1/recommend",
      expect.objectContaining({ method: "POST" }),
    );
  });
});
