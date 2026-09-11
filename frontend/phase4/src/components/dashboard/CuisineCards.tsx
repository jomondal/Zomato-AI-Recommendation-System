import type { CuisineStat } from "../../types/api";

interface CuisineCardsProps {
  cuisines: CuisineStat[];
}

const colors = ["bg-orange-100", "bg-green-100", "bg-blue-100"];

export function CuisineCards({ cuisines }: CuisineCardsProps) {
  if (!cuisines.length) {
    return (
      <div className="rounded-xl bg-white p-6 text-sm text-zomato-muted shadow-card">
        No cuisine data available.
      </div>
    );
  }

  return (
    <section className="grid gap-4 md:grid-cols-3">
      {cuisines.map((item, index) => (
        <article key={item.cuisine} className="rounded-xl bg-white p-5 shadow-card">
          <div className={`mb-4 flex h-14 w-14 items-center justify-center rounded-full ${colors[index % colors.length]}`}>
            <span className="text-xl">🍽️</span>
          </div>
          <h3 className="font-semibold text-zomato-dark">{item.cuisine}</h3>
          <p className="mt-1 text-2xl font-bold">{item.count.toLocaleString()}</p>
          <p className="text-sm text-zomato-muted">Restaurants</p>
        </article>
      ))}
    </section>
  );
}
