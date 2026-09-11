import zomatoBanner from "../../assets/zomato-banner.png";

export function ZomatoPromoBanner() {
  return (
    <div className="-mx-8 -mb-8 mt-8">
      <img
        src={zomatoBanner}
        alt="Zomato delivery banner"
        className="block w-full"
      />
    </div>
  );
}
