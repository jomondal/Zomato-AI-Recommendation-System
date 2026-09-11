import { useQuery } from "@tanstack/react-query";

import { getFilteredStats, getOverviewStats, preferencesToFilterQuery, getTopCuisines } from "../services/api";
import type { PreferenceFormValues } from "../types/api";

export function useOverviewStats() {
  return useQuery({
    queryKey: ["stats", "overview"],
    queryFn: getOverviewStats,
  });
}

export function useFilteredStats(preferences: PreferenceFormValues) {
  const filters = preferencesToFilterQuery(preferences);

  return useQuery({
    queryKey: ["stats", "filtered", filters],
    queryFn: () => getFilteredStats(filters),
  });
}

export function useTopCuisines(limit = 3) {
  return useQuery({
    queryKey: ["stats", "cuisines", limit],
    queryFn: () => getTopCuisines(limit),
  });
}
