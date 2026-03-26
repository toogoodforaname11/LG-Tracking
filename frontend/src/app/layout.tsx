import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "BC Local Government Council Tracker – Housing, Transit & Provincial Priority Updates",
  description:
    "Subscribe to updates on housing, transit, and local government hearings from BC municipalities.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50 text-gray-900 antialiased">
        <header className="border-b bg-white px-6 py-4">
          <div className="mx-auto flex max-w-2xl items-center justify-between">
            <div>
              <h1 className="text-xl font-bold text-blue-800">
                                    BC Local Government Council Tracker
              </h1>
              <p className="text-xs text-gray-500">
                Municipal Council Alerts &amp; Digest
              </p>
            </div>
            <div className="flex items-center gap-3">
              <Link
                href="/feedback"
                className="text-sm text-blue-600 hover:text-blue-800 hover:underline"
              >
                Feedback
              </Link>
              <span className="rounded bg-amber-100 px-2 py-1 text-xs font-medium text-amber-800">
                Experimental
              </span>
            </div>
          </div>
        </header>
        <main className="mx-auto max-w-2xl px-6 py-8">{children}</main>
        <footer className="border-t bg-gray-100 px-6 py-6">
          <div className="mx-auto max-w-2xl">
            <p className="text-xs leading-relaxed text-gray-500">
              This is an experimental personal tool using public data. AI
              summaries may contain errors. Always verify with original
              municipal sources. Not official government communication. This
              tool tracks publicly available council meeting agendas, minutes,
              and videos from BC municipalities.
            </p>
            <p className="mt-2 text-xs text-gray-500">
              <Link
                href="/feedback"
                className="text-blue-600 hover:text-blue-800 hover:underline"
              >
                Report Issues / Share Ideas
              </Link>
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}
