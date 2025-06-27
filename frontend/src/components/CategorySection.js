import React from 'react';

const CATEGORY_ICONS = {
  International: '/globe.svg',
  Indian: '/file.svg',
  Sports: '/window.svg',
  Tech: '/next.svg',
};

export default function CategorySection({ category, articles, summary }) {
  // Split summary into sentences (naive split by period, can be improved)
  const sentences = summary.split('.').map(s => s.trim()).filter(Boolean);

  return (
    <section className="relative bg-white/70 dark:bg-gray-900/70 backdrop-blur-lg rounded-3xl shadow-2xl p-10 border border-blue-200 dark:border-gray-700 transition-all hover:scale-[1.025] hover:shadow-3xl duration-300 group overflow-hidden">
      <div className="absolute -top-8 -right-8 opacity-10 group-hover:opacity-20 transition-opacity duration-300">
        <img src={CATEGORY_ICONS[category] || '/globe.svg'} alt="icon" className="w-32 h-32" />
      </div>
      <div className="flex items-center gap-4 mb-4">
        <img src={CATEGORY_ICONS[category] || '/globe.svg'} alt="icon" className="w-10 h-10 drop-shadow-md" />
        <h2 className="text-2xl font-extrabold text-blue-900 dark:text-blue-200 tracking-tight font-playfair drop-shadow-sm">
          {category}
        </h2>
      </div>
      <div
        className="prose prose-blue dark:prose-invert max-w-none text-lg leading-relaxed font-inter"
        dangerouslySetInnerHTML={{ __html: summary }}
      />
    </section>
  );
} 