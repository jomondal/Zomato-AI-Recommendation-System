import { useState } from "react";

import { HeroBanner } from "../components/dashboard/HeroBanner";
import { ZomatoPromoBanner } from "../components/dashboard/ZomatoPromoBanner";
import { DashboardLayout } from "../components/layout/DashboardLayout";
import type { SearchSelection } from "../components/layout/CityAreaSearch";
import { AiSummary } from "../components/recommend/AiSummary";
import { PreferenceForm } from "../components/recommend/PreferenceForm";
import { RecommendationCard } from "../components/recommend/RecommendationCard";
import { useFilterOptions } from "../hooks/useFilterOptions";
import { useRecommend } from "../hooks/useRecommend";
import type { PreferenceFormValues } from "../types/api";

function createDefaultPreferences(): PreferenceFormValues {
  return {
    city: "",
    location: "",
    cuisines: [],
    minRating: 4.0,
    maxPrice: 800,
    freeText: "",
  };
}

export function DashboardPage() {
  const [citySearch, setCitySearch] = useState("");
  const [preferences, setPreferences] = useState<PreferenceFormValues>(createDefaultPreferences);

  const { data: filterOptions } = useFilterOptions();
  const recommend = useRecommend();

  const handleSearchSelect = (selection: SearchSelection) => {
    if (selection.kind === "city") {
      setPreferences((prev) => ({ ...prev, city: selection.value, location: "" }));
    } else {
      setPreferences((prev) => ({ ...prev, location: selection.value, city: "" }));
    }
  };

  const handleSubmit = () => {
    recommend.mutate(preferences);
  };

  const handleReset = () => {
    setCitySearch("");
    setPreferences(createDefaultPreferences());
    recommend.reset();
  };

  return (
    <DashboardLayout
      filterOptions={filterOptions}
      citySearch={citySearch}
      onCitySearchChange={setCitySearch}
      onSearchSelect={handleSearchSelect}
      onHomeClick={handleReset}
    >
      <HeroBanner />

      <div className="grid gap-4 sm:gap-6 lg:grid-cols-3">
        <div className="space-y-4 sm:space-y-6 lg:col-span-1">
          <PreferenceForm
            values={preferences}
            options={filterOptions}
            loading={recommend.isPending}
            onChange={setPreferences}
            onSubmit={handleSubmit}
          />
        </div>

        <div className="space-y-4 sm:space-y-6 lg:col-span-2">
          <AiSummary result={recommend.data} />
          {recommend.isError && (
            <p className="rounded-lg bg-red-50 p-4 text-sm text-red-600">
              {recommend.error.message}
            </p>
          )}
          <div className="space-y-4">
            {recommend.data?.recommendations.map((item) => (
              <RecommendationCard key={item.restaurant_id} item={item} />
            ))}
          </div>
        </div>
      </div>

      <ZomatoPromoBanner />
    </DashboardLayout>
  );
}
