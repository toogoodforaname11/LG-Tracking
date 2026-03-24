import type { Metadata } from "next";
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
        <header className="border-b bg-white px-6 py-4">
          <div className="mx-auto flex max-w-6xl items-center justify-between">
            <h1 className="text-xl font-bold">BC Hearing Watch</h1>
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
