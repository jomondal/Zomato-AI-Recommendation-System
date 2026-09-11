export interface RecommendRequest {
  city?: string;
  location?: string;
  min_rating?: number;
  max_rating?: number;
  min_price?: number;
  max_price?: number;
  cuisines?: string[];
  free_text?: string;
  use_llm?: boolean;
  limit?: number;
}

export interface RecommendationItem {
  rank: number;
  restaurant_id: number;
  name: string;
  rating: number | null;
  votes: number;
  cost_for_two: number | null;
  location: string | null;
  city: string | null;
  cuisines: string | null;
  match_score: number;
  reason: string;
  highlights: string[];
  url: string | null;
  online_order: boolean;
  book_table: boolean;
}

export interface RecommendResponse {
  summary: string;
  total_candidates: number;
  recommendations: RecommendationItem[];
  latency_ms: number;
  source: string;
  llm_latency_ms: number | null;
}

export interface OverviewStats {
  total_restaurants: number;
  restaurants_with_rating: number;
  average_rating: number | null;
  average_cost_for_two: number | null;
  total_cities: number;
  total_cuisines: number;
}

export interface FilteredStats {
  total_restaurants: number;
  average_rating: number | null;
  average_cost_for_two: number | null;
  total_cities: number;
}

export interface FilterQuery {
  city?: string;
  location?: string;
  min_rating?: number;
  max_price?: number;
  cuisines?: string[];
}

export interface CuisineStat {
  cuisine: string;
  count: number;
}

export interface FilterOptions {
  cities: string[];
  locations: string[];
  cuisines: string[];
  price_ranges: { label: string; min: number; max: number }[];
  rating_range: { min: number; max: number };
}

export interface PreferenceFormValues {
  city: string;
  location: string;
  cuisines: string[];
  minRating: number;
  maxPrice: number;
  freeText: string;
}
