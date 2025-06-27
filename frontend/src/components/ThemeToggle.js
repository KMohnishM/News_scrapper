"use client";
import { useEffect, useState } from "react";

export default function ThemeToggle() {
  const [theme, setTheme] = useState("light");

  useEffect(() => {
    // On mount, check localStorage or system preference
    const stored = localStorage.getItem("theme");
    if (stored) {
      setTheme(stored);
      document.documentElement.classList.toggle("dark", stored === "dark");
    } else if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
      setTheme("dark");
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, []);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", theme === "dark");
  }, [theme]);

  const toggleTheme = () => {
    const newTheme = theme === "dark" ? "light" : "dark";
    setTheme(newTheme);
    localStorage.setItem("theme", newTheme);
  };

  return (
    <button
      aria-label="Toggle dark mode"
      onClick={toggleTheme}
      className="relative w-14 h-8 rounded-full bg-blue-200 dark:bg-gray-700 flex items-center px-1 transition-colors duration-300 shadow-md border border-blue-300 dark:border-gray-600 focus:outline-none"
    >
      <span
        className={`absolute left-1 top-1 w-6 h-6 rounded-full bg-white dark:bg-gray-900 shadow transform transition-transform duration-300 ${theme === "dark" ? "translate-x-6" : "translate-x-0"}`}
      />
      <span className="absolute left-2 top-2 w-4 h-4 text-yellow-400">
        {/* Sun icon */}
        <svg className={`w-4 h-4 ${theme === "dark" ? "opacity-0" : "opacity-100"} transition-opacity duration-300`} fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="5"/><path d="M12 1v2m0 18v2m11-11h-2M3 12H1m16.95 7.07l-1.41-1.41M6.34 6.34L4.93 4.93m12.02 0l-1.41 1.41M6.34 17.66l-1.41 1.41"/></svg>
      </span>
      <span className="absolute right-2 top-2 w-4 h-4 text-blue-900 dark:text-blue-200">
        {/* Moon icon */}
        <svg className={`w-4 h-4 ${theme === "dark" ? "opacity-100" : "opacity-0"} transition-opacity duration-300`} fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M21 12.79A9 9 0 1111.21 3a7 7 0 109.79 9.79z"/></svg>
      </span>
    </button>
  );
} 