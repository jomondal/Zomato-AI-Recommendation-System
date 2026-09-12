import zomatoBanner from "../../assets/zomato-banner.png";

export function ZomatoPromoBanner() {
  return (
    <div className="-mx-4 -mb-4 mt-6 sm:-mx-6 sm:-mb-6 sm:mt-8 lg:-mx-8 lg:-mb-8">
      <img
        src={zomatoBanner}
        alt="Zomato delivery banner"
        className="block h-auto w-full max-w-none object-cover object-center"
      />
    </div>
  );
}
