import zomatoLogo from "../../assets/zomato-logo.png";

interface ZomatoLogoProps {
  className?: string;
  alt?: string;
}

export function ZomatoLogo({ className = "h-8 w-auto", alt = "Zomato" }: ZomatoLogoProps) {
  return <img src={zomatoLogo} alt={alt} className={`object-contain ${className}`} />;
}
