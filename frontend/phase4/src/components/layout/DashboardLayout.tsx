import type { ReactNode } from "react";

import type { FilterOptions } from "../../types/api";

import { Header } from "./Header";
import { Sidebar } from "./Sidebar";
import type { SearchSelection } from "./CityAreaSearch";

interface DashboardLayoutProps {
  children: ReactNode;
  filterOptions?: FilterOptions;
  citySearch: string;
  onCitySearchChange: (value: string) => void;
  onSearchSelect: (selection: SearchSelection) => void;
  onHomeClick: () => void;
}

export function DashboardLayout({
  children,
  filterOptions,
  citySearch,
  onCitySearchChange,
  onSearchSelect,
  onHomeClick,
}: DashboardLayoutProps) {
  return (
    <div className="flex min-h-screen min-w-0">
      <Sidebar onHomeClick={onHomeClick} />
      <div className="flex min-w-0 flex-1 flex-col">
        <Header
          filterOptions={filterOptions}
          citySearch={citySearch}
          onCitySearchChange={onCitySearchChange}
          onSearchSelect={onSearchSelect}
          onHomeClick={onHomeClick}
        />
        <main className="flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-6 lg:p-8">
          {children}
        </main>
      </div>
    </div>
  );
}
