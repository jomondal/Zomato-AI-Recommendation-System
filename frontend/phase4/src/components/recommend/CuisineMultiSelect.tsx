import { ChevronDown } from "lucide-react";
import { useEffect, useRef, useState } from "react";

interface CuisineMultiSelectProps {
  options: string[];
  value: string[];
  onChange: (value: string[]) => void;
}

function formatSelection(value: string[]) {
  if (value.length === 0) return "Any cuisine";
  if (value.length <= 2) return value.join(", ");
  return `${value.slice(0, 2).join(", ")} +${value.length - 2} more`;
}

export function CuisineMultiSelect({ options, value, onChange }: CuisineMultiSelectProps) {
  const [open, setOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

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

  const toggle = (cuisine: string) => {
    onChange(
      value.includes(cuisine) ? value.filter((item) => item !== cuisine) : [...value, cuisine],
    );
  };

  return (
    <div ref={containerRef} className="relative mt-1">
      <button
        type="button"
        aria-haspopup="listbox"
        aria-expanded={open}
        onClick={() => setOpen((prev) => !prev)}
        className="flex w-full items-center justify-between rounded-lg border border-gray-200 px-3 py-2 text-left text-sm"
      >
        <span className={value.length ? "text-zomato-dark" : "text-zomato-muted"}>
          {formatSelection(value)}
        </span>
        <ChevronDown
          size={16}
          className={`text-zomato-muted transition ${open ? "rotate-180" : ""}`}
        />
      </button>

      {open && (
        <div
          role="listbox"
          aria-multiselectable="true"
          className="absolute z-20 mt-1 max-h-48 w-full overflow-y-auto rounded-lg border border-gray-200 bg-white py-1 shadow-card"
        >
          {options.map((cuisine) => (
            <label
              key={cuisine}
              className="flex cursor-pointer items-center gap-2 px-3 py-2 text-sm hover:bg-gray-50"
            >
              <input
                type="checkbox"
                checked={value.includes(cuisine)}
                onChange={() => toggle(cuisine)}
                className="accent-zomato-red"
              />
              {cuisine}
            </label>
          ))}
          <div className="border-t border-gray-100 px-3 py-2">
            <button
              type="button"
              onClick={() => setOpen(false)}
              className="w-full rounded-md bg-zomato-red py-1.5 text-xs font-semibold text-white"
            >
              Done
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
