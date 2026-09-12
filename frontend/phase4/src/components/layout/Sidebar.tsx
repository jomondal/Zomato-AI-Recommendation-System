import { Home } from "lucide-react";

interface SidebarProps {
  onHomeClick: () => void;
}

export function Sidebar({ onHomeClick }: SidebarProps) {
  return (
    <aside className="hidden w-14 shrink-0 flex-col items-center border-r border-gray-200 bg-white py-5 sm:flex sm:w-16 sm:py-6">
      <button
        type="button"
        title="Reset and start over"
        onClick={onHomeClick}
        className="flex h-10 w-10 items-center justify-center rounded-full bg-zomato-red text-white shadow-card transition hover:bg-red-600"
      >
        <Home size={20} />
      </button>
    </aside>
  );
}