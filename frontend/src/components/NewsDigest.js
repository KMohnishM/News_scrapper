"use client";
import { useEffect, useState } from "react";

const COLORS = [
  "text-emerald-400",
  "text-sky-400",
  "text-fuchsia-400",
  "text-amber-400",
  "text-indigo-400",
  "text-rose-400",
  "text-cyan-400",
  "text-lime-400",
];

function colorizeParagraph(paragraph) {
  // Split by <a ...>...</a> and wrap each in a span with a color
  const linkRegex = /(<a [^>]+>.*?<\/a>)/g;
  const parts = paragraph.split(linkRegex).filter(Boolean);
  let colorIdx = 0;
  return parts.map((part, idx) => {
    if (part.startsWith("<a ")) {
      const colorClass = COLORS[colorIdx % COLORS.length];
      colorIdx++;
      return (
        <span key={idx} className={colorClass + " font-semibold hover:underline transition-all duration-200"} dangerouslySetInnerHTML={{ __html: part + ' ' }} />
      );
    }
    return <span key={idx} dangerouslySetInnerHTML={{ __html: part }} />;
  });
}

export default function NewsDigest() {
  const [sections, setSections] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchSections() {
      try {
        const res = await fetch("http://localhost:8000/api/digests/sections/");
        if (!res.ok) throw new Error("Failed to fetch digest sections");
        const data = await res.json();
        setSections(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchSections();
  }, []);

  if (loading) return <div className="text-gray-400">Loading...</div>;
  if (error) return <div className="text-rose-400">{error}</div>;
  if (!sections.length) return <div className="text-gray-400">No digest available.</div>;

  return (
    <div className="w-full grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
      {sections.map(({ category, paragraph }, i) => (
        <section
          key={category}
          className="relative bg-black/90 rounded-3xl shadow-2xl p-8 border border-gray-800/80 backdrop-blur-lg overflow-hidden group hover:scale-[1.025] transition-transform duration-300 flex flex-col"
        >
          <div className={`absolute left-0 top-0 h-2 w-full rounded-t-3xl ${COLORS[i % COLORS.length]} bg-gradient-to-r from-transparent via-emerald-400/40 to-transparent group-hover:opacity-80 transition-opacity duration-300 z-10`} />
          <h2 className="relative z-10 text-2xl font-extrabold text-emerald-200 mb-4 tracking-tight drop-shadow-lg">
            {category}
          </h2>
          <div className="relative z-10 prose prose-invert max-w-none text-lg leading-relaxed flex-1">
            {colorizeParagraph(paragraph)}
          </div>
        </section>
      ))}
    </div>
  );
} 