import { Home } from "lucide-react";

import type { FilterOptions } from "../../types/api";

import { CityAreaSearch, type SearchSelection } from "./CityAreaSearch";
import { ZomatoLogo } from "./ZomatoLogo";

interface HeaderProps {
  filterOptions?: FilterOptions;
  citySearch: string;
  onCitySearchChange: (value: string) => void;
  onSearchSelect: (selection: SearchSelection) => void;
  onHomeClick: () => void;
}

export function Header({
  filterOptions,
  citySearch,
  onCitySearchChange,
  onSearchSelect,
  onHomeClick,
}: HeaderProps) {
  return (
    <header className="border-b border-gray-200 bg-white px-4 py-4 sm:px-6 lg:px-8 lg:py-5">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div className="flex min-w-0 items-center gap-2 sm:gap-3">
          <button
            type="button"
            title="Reset and start over"
            onClick={onHomeClick}
            className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-zomato-red text-white shadow-card transition hover:bg-red-600 sm:hidden"
          >
            <Home size={18} />
          </button>
          <ZomatoLogo className="h-8 w-auto shrink-0 sm:h-10" />
          <h1 className="truncate font-zomato text-lg font-black italic leading-none tracking-tight text-zomato-red sm:text-[1.35rem]">
            AI Recommender
          </h1>
        </div>
        <div className="w-full min-w-0 lg:max-w-md lg:flex-shrink-0">
          <CityAreaSearch
            options={filterOptions}
            value={citySearch}
            onChange={onCitySearchChange}
            onSelect={onSearchSelect}
          />
        </div>
      </div>
    </header>
  );
}
