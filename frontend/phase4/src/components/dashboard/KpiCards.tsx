import type { FilteredStats } from "../../types/api";

interface KpiCardsProps {
  stats?: FilteredStats;
  loading?: boolean;
}

const formatNumber = (value: number | null | undefined, suffix = "") => {
  if (value == null) return "—";
  if (value >= 1_000_000) return `${(value / 1_000_000).toFixed(1)}M${suffix}`;
  if (value >= 1_000) return `${(value / 1_000).toFixed(1)}K${suffix}`;
  return `${value}${suffix}`;
};

export function KpiCards({ stats, loading = false }: KpiCardsProps) {
  const placeholder = loading ? "..." : "—";
  const items = [
    {
      label: "Matching Restaurants",
      value: stats ? formatNumber(stats.total_restaurants) : placeholder,
    },
    { label: "Avg Rating", value: stats?.average_rating?.toFixed(1) ?? placeholder },
    {
      label: "Avg Price (₹)",
      value: stats?.average_cost_for_two != null ? formatNumber(stats.average_cost_for_two) : placeholder,
    },
    { label: "Total Cities", value: stats ? formatNumber(stats.total_cities) : placeholder },
  ];

  return (
    <section className="grid grid-cols-2 gap-4">
      {items.map((item) => (
        <div key={item.label} className="rounded-xl bg-white p-5 shadow-card">
          <p className="text-sm text-zomato-muted">{item.label}</p>
          <p className="mt-2 text-3xl font-bold text-zomato-dark">{item.value}</p>
        </div>
      ))}
    </section>
  );
}
