import type {
  CuisineStat,
  FilteredStats,
  FilterOptions,
  FilterQuery,
  OverviewStats,
  PreferenceFormValues,
  RecommendRequest,
  RecommendResponse,
} from "../types/api";

const API_BASE = import.meta.env.VITE_API_URL ?? "";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...(options?.headers ?? {}) },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`API error ${response.status}: ${response.statusText}`);
  }

  return response.json() as Promise<T>;
}

export function getOverviewStats(): Promise<OverviewStats> {
  return request<OverviewStats>("/api/v1/stats/overview");
}

function buildFilterQuery(filters: FilterQuery): string {
  const params = new URLSearchParams();

  if (filters.city) params.set("city", filters.city);
  if (filters.location) params.set("location", filters.location);
  if (filters.min_rating != null) params.set("min_rating", String(filters.min_rating));
  if (filters.max_price != null) params.set("max_price", String(filters.max_price));
  filters.cuisines?.forEach((cuisine) => params.append("cuisines", cuisine));

  const query = params.toString();
  return query ? `?${query}` : "";
}

export function preferencesToFilterQuery(values: PreferenceFormValues): FilterQuery {
  return {
    city: values.city || undefined,
    location: values.location || undefined,
    min_rating: values.minRating,
    max_price: values.maxPrice,
    cuisines: values.cuisines.length ? values.cuisines : undefined,
  };
}

export function getFilteredStats(filters: FilterQuery): Promise<FilteredStats> {
  return request<FilteredStats>(`/api/v1/stats/filtered${buildFilterQuery(filters)}`);
}

export function getTopCuisines(limit = 3): Promise<{ items: CuisineStat[] }> {
  return request<{ items: CuisineStat[] }>(`/api/v1/stats/cuisines?limit=${limit}`);
}

export function getFilterOptions(): Promise<FilterOptions> {
  return request<FilterOptions>("/api/v1/filters/options");
}

export function postRecommend(body: RecommendRequest): Promise<RecommendResponse> {
  return request<RecommendResponse>("/api/v1/recommend", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

export function toRecommendRequest(
  values: {
    city: string;
    location: string;
    cuisines: string[];
    minRating: number;
    maxPrice: number;
    freeText: string;
  },
  limit = 5,
): RecommendRequest {
  return {
    city: values.city || undefined,
    location: values.location || undefined,
    min_rating: values.minRating,
    max_price: values.maxPrice,
    cuisines: values.cuisines.length ? values.cuisines : [],
    free_text: values.freeText || undefined,
    use_llm: true,
    limit,
  };
}
