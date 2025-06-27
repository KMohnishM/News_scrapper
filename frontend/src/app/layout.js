import "./globals.css";
import Header from "../components/Header";
import Footer from "../components/Footer";
import { Inter } from "next/font/google";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });

export const metadata = {
  title: "News Digest",
  description: "Your daily world & India news, summarized.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className="bg-black text-white min-h-screen">
      <body className="bg-black min-h-screen font-sans antialiased" style={{ background: "linear-gradient(135deg, #000 60%, #111 100%)" }}>
        <Header />
        <main className="min-h-screen w-full flex flex-col items-center justify-start bg-black">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}
