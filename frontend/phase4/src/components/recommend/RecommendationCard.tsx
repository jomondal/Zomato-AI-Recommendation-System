import { ExternalLink, Star } from "lucide-react";

import type { RecommendationItem } from "../../types/api";

interface RecommendationCardProps {
  item: RecommendationItem;
}

export function RecommendationCard({ item }: RecommendationCardProps) {
  return (
    <article className="rounded-xl border border-gray-100 bg-white p-5 shadow-card">
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="flex items-center gap-2">
            <span className="rounded-full bg-zomato-red/10 px-2 py-0.5 text-xs font-semibold text-zomato-red">
              #{item.rank}
            </span>
            <h3 className="text-lg font-semibold">{item.name}</h3>
          </div>
          <p className="mt-1 text-sm text-zomato-muted">
            {item.location ?? item.city} · {item.cuisines}
          </p>
        </div>
        <div className="text-right">
          <p className="flex items-center justify-end gap-1 font-semibold text-zomato-red">
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
