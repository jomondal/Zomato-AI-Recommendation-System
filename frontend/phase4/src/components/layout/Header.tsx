import type { FilterOptions } from "../../types/api";

import { CityAreaSearch, type SearchSelection } from "./CityAreaSearch";
import { ZomatoLogo } from "./ZomatoLogo";

interface HeaderProps {
  filterOptions?: FilterOptions;
  citySearch: string;
  onCitySearchChange: (value: string) => void;
  onSearchSelect: (selection: SearchSelection) => void;
}

export function Header({
  filterOptions,
  citySearch,
  onCitySearchChange,
  onSearchSelect,
}: HeaderProps) {
  return (
    <header className="flex items-center justify-between border-b border-gray-200 bg-white px-8 py-5">
      <div className="flex items-center gap-3">
        <ZomatoLogo className="h-10 w-auto shrink-0" />
        <h1 className="font-zomato text-[1.35rem] font-black italic leading-none tracking-tight text-zomato-red">
          AI Recommender
        </h1>
      </div>
      <CityAreaSearch
        options={filterOptions}
        value={citySearch}
        onChange={onCitySearchChange}
        onSelect={onSearchSelect}
      />
    </header>
  );
}
