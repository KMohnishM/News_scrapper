import React from "react";

export default function Header() {
  return (
    <header className="fixed top-0 left-0 w-full flex flex-col items-center py-4 bg-black/70 backdrop-blur-lg border-b border-gray-800 shadow-lg z-50">
      <div className="flex items-center gap-4 w-full max-w-7xl px-4">
        <img src="/globe.svg" alt="Logo" className="w-10 h-10 drop-shadow-lg" />
        <h1 className="text-2xl sm:text-3xl font-extrabold text-emerald-300 tracking-tight drop-shadow-[0_0_16px_#34d399]">
          NewsDigest
        </h1>
        <nav className="ml-auto flex gap-6">
          <a href="#" className="text-gray-300 hover:text-emerald-400 font-medium transition">Home</a>
          <a href="#" className="text-gray-300 hover:text-emerald-400 font-medium transition">About</a>
          <a href="#" className="text-gray-300 hover:text-emerald-400 font-medium transition">Contact</a>
        </nav>
      </div>
    </header>
  );
} 