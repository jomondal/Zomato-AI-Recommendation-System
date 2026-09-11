import type { RecommendResponse } from "../../types/api";

interface AiSummaryProps {
  result?: RecommendResponse;
}

export function AiSummary({ result }: AiSummaryProps) {
  if (!result) {
    return (
      <div className="rounded-xl bg-white p-6 text-sm text-zomato-muted shadow-card">
        Set your preferences and click <strong>Get AI Picks</strong> to see recommendations.
      </div>
    );
  }

  return (
    <section className="rounded-xl bg-white p-6 shadow-card">
      <h2 className="mb-2 text-lg font-semibold">AI Recommendations</h2>
      <p className="text-sm leading-relaxed text-zomato-muted">{result.summary}</p>
    </section>
  );
}
