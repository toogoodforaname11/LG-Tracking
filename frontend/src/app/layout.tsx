import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "BC Local Government Council Tracker",
  description:
    "Subscribe to alerts and weekly digests from BC municipal council meetings.",
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
            <span className="rounded bg-gray-100 px-2 py-1 text-xs font-medium text-gray-500">
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
