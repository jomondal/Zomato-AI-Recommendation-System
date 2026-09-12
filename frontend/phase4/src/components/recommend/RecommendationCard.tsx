import { ExternalLink, Star } from "lucide-react";

import type { RecommendationItem } from "../../types/api";

interface RecommendationCardProps {
  item: RecommendationItem;
}

export function RecommendationCard({ item }: RecommendationCardProps) {
  return (
    <article className="rounded-xl border border-gray-100 bg-white p-4 shadow-card sm:p-5">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-center gap-2">
            <span className="rounded-full bg-zomato-red/10 px-2 py-0.5 text-xs font-semibold text-zomato-red">
              #{item.rank}
            </span>
            <h3 className="text-base font-semibold sm:text-lg">{item.name}</h3>
          </div>
          <p className="mt-1 break-words text-sm text-zomato-muted">
            {item.location ?? item.city} · {item.cuisines}
          </p>
        </div>
        <div className="flex shrink-0 items-center justify-between gap-4 sm:block sm:text-right">
          <p className="flex items-center gap-1 font-semibold text-zomato-red sm:justify-end">
            <Star size={16} fill="#E23744" color="#E23744" />
            {item.rating?.toFixed(1) ?? "—"}
          </p>
          <p className="text-sm text-zomato-muted">
            {item.cost_for_two ? `₹${item.cost_for_two}` : "—"} for two
          </p>
        </div>
      </div>

      <p className="mt-3 text-sm leading-relaxed text-zomato-dark">{item.reason}</p>

      <div className="mt-3 flex flex-wrap gap-2">
        {item.highlights.map((highlight) => (
          <span
            key={highlight}
            className="rounded-full bg-gray-100 px-2.5 py-1 text-xs text-zomato-muted"
          >
            {highlight}
          </span>
        ))}
        <span className="rounded-full bg-zomato-red/10 px-2.5 py-1 text-xs font-medium text-zomato-red">
          {item.match_score}% match
        </span>
      </div>

      {item.url && (
        <a
          href={item.url}
          target="_blank"
          rel="noreferrer"
          className="mt-4 inline-flex items-center gap-1 text-sm font-medium text-zomato-red hover:underline"
        >
          View on Zomato <ExternalLink size={14} />
        </a>
      )}
    </article>
  );
}
