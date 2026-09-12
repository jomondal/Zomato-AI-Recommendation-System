import type { FilterOptions, PreferenceFormValues } from "../../types/api";

import { CuisineMultiSelect } from "./CuisineMultiSelect";

interface PreferenceFormProps {
  values: PreferenceFormValues;
  options?: FilterOptions;
  loading?: boolean;
  onChange: (values: PreferenceFormValues) => void;
  onSubmit: () => void;
}

export function PreferenceForm({
  values,
  options,
  loading = false,
  onChange,
  onSubmit,
}: PreferenceFormProps) {
  const update = (patch: Partial<PreferenceFormValues>) => onChange({ ...values, ...patch });

  return (
    <form
      className="rounded-xl bg-white p-4 shadow-card sm:p-6"
      onSubmit={(e) => {
        e.preventDefault();
        onSubmit();
      }}
    >
      <h2 className="mb-4 text-lg font-semibold">Your Preferences</h2>

      <label className="mb-3 block text-sm font-medium">
        City
        <select
          value={values.city}
          onChange={(e) => update({ city: e.target.value, location: "" })}
          className="mt-1 w-full rounded-lg border border-gray-200 px-3 py-2 text-sm"
        >
          <option value="">All cities</option>
          {options?.cities.map((city) => (
            <option key={city} value={city}>{city}</option>
          ))}
        </select>
      </label>

      <div className="mb-3">
        <span className="block text-sm font-medium">Cuisines</span>
        <CuisineMultiSelect
          options={options?.cuisines ?? []}
          value={values.cuisines}
          onChange={(cuisines) => update({ cuisines })}
        />
      </div>

      <label className="mb-3 block text-sm font-medium">
        Min Rating: {values.minRating.toFixed(1)}★
        <input
          type="range"
          min={options?.rating_range.min ?? 0}
          max={options?.rating_range.max ?? 5}
          step={0.1}
          value={values.minRating}
          onChange={(e) => update({ minRating: Number(e.target.value) })}
          className="mt-2 w-full accent-zomato-red"
        />
      </label>

      <label className="mb-3 block text-sm font-medium">
        Max Price (₹ for two): {values.maxPrice}
        <input
          type="range"
          min={100}
          max={2000}
          step={50}
          value={values.maxPrice}
          onChange={(e) => update({ maxPrice: Number(e.target.value) })}
          className="mt-2 w-full accent-zomato-red"
        />
      </label>

      <label className="mb-4 block text-sm font-medium">
        Describe your preference
        <textarea
          value={values.freeText}
          onChange={(e) => update({ freeText: e.target.value })}
          placeholder="e.g. rooftop ambience, family dinner"
          className="mt-1 w-full rounded-lg border border-gray-200 px-3 py-2 text-sm"
          rows={2}
        />
      </label>

      <button
        type="submit"
        disabled={loading}
        className="w-full rounded-lg bg-zomato-red py-3 text-sm font-semibold text-white transition hover:bg-red-600 disabled:opacity-60"
      >
        {loading ? "Getting AI Picks..." : "Get AI Picks"}
      </button>
    </form>
  );
}
