import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "NCDIPS - Customs Intelligence",
  description: "Nigeria Customs Declaration Intelligence & Profiling System",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased bg-slate-50 text-slate-900">
        {children}
      </body>
    </html>
  );
}
