import { Search } from "lucide-react";
import { useEffect, useMemo, useRef, useState, type KeyboardEvent } from "react";

import type { FilterOptions } from "../../types/api";

export type SearchSelection =
  | { kind: "city"; value: string }
  | { kind: "location"; value: string };

interface CityAreaSearchProps {
  options?: FilterOptions;
  value: string;
  onChange: (value: string) => void;
  onSelect: (selection: SearchSelection) => void;
}

const RESULT_LIMIT = 8;

export function CityAreaSearch({ options, value, onChange, onSelect }: CityAreaSearchProps) {
  const [open, setOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  const results = useMemo(() => {
    const query = value.trim().toLowerCase();
    if (!query || !options) return [];

    const cityMatches = options.cities
      .filter((city) => city.toLowerCase().includes(query))
      .slice(0, RESULT_LIMIT)
      .map((city) => ({ kind: "city" as const, value: city, label: city, group: "Cities" }));

    const locationMatches = options.locations
      .filter((location) => location.toLowerCase().includes(query))
      .slice(0, RESULT_LIMIT)
      .map((location) => ({
        kind: "location" as const,
        value: location,
        label: location,
        group: "Areas",
      }));

    return [...cityMatches, ...locationMatches];
  }, [options, value]);

  useEffect(() => {
    if (!open) return;

    const handleClickOutside = (event: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [open]);

  const handleSelect = (selection: SearchSelection) => {
    onSelect(selection);
    onChange(selection.value);
    setOpen(false);
  };

  const handleKeyDown = (event: KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter" && results.length > 0) {
      event.preventDefault();
      handleSelect({ kind: results[0].kind, value: results[0].value });
    }

    if (event.key === "Escape") {
      setOpen(false);
    }
  };

  return (
    <div ref={containerRef} className="relative w-full max-w-xs">
      <Search className="absolute left-3 top-1/2 z-10 -translate-y-1/2 text-zomato-muted" size={18} />
      <input
        type="text"
        role="combobox"
        aria-expanded={open}
        aria-autocomplete="list"
        placeholder="Search city or area..."
        value={value}
        onChange={(e) => {
          onChange(e.target.value);
          setOpen(true);
        }}
        onFocus={() => setOpen(true)}
        onKeyDown={handleKeyDown}
        className="w-full rounded-lg border border-gray-200 py-2.5 pl-10 pr-4 text-sm outline-none focus:border-zomato-red"
      />

      {open && value.trim() && (
        <div className="absolute z-20 mt-1 max-h-64 w-full overflow-y-auto rounded-lg border border-gray-200 bg-white py-1 shadow-card">
          {results.length > 0 ? (
            results.map((result) => (
              <button
                key={`${result.kind}-${result.value}`}
                type="button"
                onMouseDown={(e) => e.preventDefault()}
                onClick={() => handleSelect({ kind: result.kind, value: result.value })}
                className="flex w-full items-center justify-between px-3 py-2 text-left text-sm hover:bg-gray-50"
              >
                <span>{result.label}</span>
                <span className="text-xs text-zomato-muted">{result.group}</span>
              </button>
            ))
          ) : (
            <p className="px-3 py-2 text-sm text-zomato-muted">No matching cities or areas.</p>
          )}
        </div>
      )}
    </div>
  );
}
