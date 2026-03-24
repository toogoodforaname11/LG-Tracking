import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "BC Hearing Watch",
  description: "Track BC local government council hearing updates",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="bg-gray-50 text-gray-900 antialiased">
        <header className="border-b bg-white px-6 py-3">
          <div className="mx-auto flex max-w-6xl items-center justify-between">
            <div className="flex items-center gap-6">
              <Link href="/" className="text-xl font-bold hover:text-blue-700">
                BC Hearing Watch
              </Link>
              <nav className="flex gap-4 text-sm">
                <Link
                  href="/"
                  className="text-gray-600 hover:text-gray-900"
                >
                  Dashboard
                </Link>
                <Link
                  href="/municipalities"
                  className="text-gray-600 hover:text-gray-900"
                >
                  Municipalities
                </Link>
                <Link
                  href="/tracks/new"
                  className="text-gray-600 hover:text-gray-900"
                >
                  New Track
                </Link>
                <Link
                  href="/search"
                  className="text-gray-600 hover:text-gray-900"
                >
                  Search
                </Link>
              </nav>
            </div>
            <span className="rounded bg-amber-100 px-2 py-1 text-xs font-medium text-amber-800">
              Prototype
            </span>
          </div>
        </header>
        <main className="mx-auto max-w-6xl px-6 py-8">{children}</main>
      </body>
    </html>
  );
}
