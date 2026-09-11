import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { PreferenceForm } from "../src/components/recommend/PreferenceForm";

const options = {
  cities: ["Banashankari", "BTM"],
  locations: ["Banashankari"],
  cuisines: ["Italian", "North Indian"],
  price_ranges: [{ label: "Budget", min: 0, max: 400 }],
  rating_range: { min: 0, max: 5 },
};

describe("PreferenceForm", () => {
  it("renders fields and calls onSubmit", async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    const onChange = vi.fn();

    render(
      <PreferenceForm
        values={{
          city: "Banashankari",
          location: "",
          cuisines: ["Italian"],
          minRating: 4.0,
          maxPrice: 700,
          freeText: "pizza",
        }}
        options={options}
        onChange={onChange}
        onSubmit={onSubmit}
      />,
    );

    expect(screen.getByText("Your Preferences")).toBeInTheDocument();
    expect(screen.getByDisplayValue("Banashankari")).toBeInTheDocument();
    expect(screen.getByDisplayValue("pizza")).toBeInTheDocument();

    await user.click(screen.getByRole("button", { name: /Get AI Picks/i }));
    expect(onSubmit).toHaveBeenCalledTimes(1);
  });

  it("updates cuisines via onChange", async () => {
    const user = userEvent.setup();
    const onChange = vi.fn();

    render(
      <PreferenceForm
        values={{
          city: "",
          location: "",
          cuisines: [],
          minRating: 4.0,
          maxPrice: 800,
          freeText: "",
        }}
        options={options}
        onChange={onChange}
        onSubmit={vi.fn()}
      />,
    );

    await user.click(screen.getByRole("button", { name: /Any cuisine/i }));
    await user.click(screen.getByRole("checkbox", { name: "Italian" }));
    await user.click(screen.getByRole("checkbox", { name: "North Indian" }));
    expect(onChange).toHaveBeenCalled();
  });
});
