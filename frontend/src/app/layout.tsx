import type { Metadata } from "next";
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
            <div className="flex items-center gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-blue-800">
                <svg className="h-5 w-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
              <div>
                <h1 className="text-xl font-bold text-blue-800">
                  BC Local Government Council Tracker
                </h1>
                <p className="text-xs text-gray-500">
                  Housing, Transit &amp; Policy Monitoring for BC Municipalities
                </p>
              </div>
            </div>
            <span className="rounded bg-amber-100 px-2 py-1 text-xs font-medium text-amber-800">
              Experimental
            </span>
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
          </div>
        </footer>
      </body>
    </html>
  );
}
