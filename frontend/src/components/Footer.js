import React from "react";

export default function Footer() {
  return (
    <footer className="w-full py-6 flex flex-col items-center bg-black/70 backdrop-blur-lg border-t border-gray-800 mt-16">
      <p className="text-sm text-gray-500">
        &copy; {new Date().getFullYear()} NewsDigest. All rights reserved.
      </p>
      <div className="flex gap-4 mt-2">
        <a href="https://nextjs.org" target="_blank" rel="noopener noreferrer" className="hover:underline text-emerald-400 text-xs">Built with Next.js</a>
        <a href="https://github.com/" target="_blank" rel="noopener noreferrer" className="hover:underline text-emerald-400 text-xs">GitHub</a>
      </div>
    </footer>
  );
} 