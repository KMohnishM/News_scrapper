import NewsDigest from '../components/NewsDigest';

export default function Home() {
  return (
    <section className="w-full max-w-7xl mx-auto flex flex-col items-center pt-28 pb-12 px-2 sm:px-6">
      <h2 className="text-4xl sm:text-5xl font-extrabold mb-12 text-center text-emerald-300 tracking-tight drop-shadow-[0_0_16px_#34d399]">
        Today's Top Stories
      </h2>
      <NewsDigest />
    </section>
  );
}
