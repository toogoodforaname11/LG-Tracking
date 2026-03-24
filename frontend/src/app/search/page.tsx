"use client";

import { useState } from "react";
import { getDocuments } from "@/lib/api";

interface DocResult {
  id: number;
  municipality_id: number;
  doc_type: string;
  title: string;
  url: string;
  is_new: boolean;
  is_processed: boolean;
  first_seen_at: string;
}

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<DocResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setSearched(true);

    try {
      // For now, fetch all documents and filter client-side
      // Phase 6 will add proper vector RAG search via Pinecone
      const docs = (await getDocuments()) as DocResult[];
      const q = query.toLowerCase();
      const filtered = q
        ? docs.filter(
            (d) =>
              d.title?.toLowerCase().includes(q) ||
              d.doc_type?.toLowerCase().includes(q) ||
              d.url?.toLowerCase().includes(q)
          )
        : docs;
      setResults(filtered);
    } catch {
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2 className="mb-6 text-2xl font-bold">Search Documents</h2>

      <form onSubmit={handleSearch} className="mb-6 flex gap-3">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search agendas, minutes, videos..."
          className="flex-1 rounded-lg border px-4 py-2 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
        />
        <button
          type="submit"
          disabled={loading}
          className="rounded-lg bg-blue-600 px-6 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? "Searching..." : "Search"}
        </button>
      </form>

      <p className="mb-4 text-xs text-gray-400">
        Currently uses keyword search on discovered documents. Vector RAG search
        (Pinecone + Gemini embeddings) will be added in a future phase.
      </p>

      {searched && results.length === 0 && (
        <div className="rounded-lg border-2 border-dashed p-8 text-center text-gray-500">
          No documents found. Try running &quot;Poll Sources&quot; from the dashboard first.
        </div>
      )}

      {results.length > 0 && (
        <div className="space-y-3">
          <p className="text-sm text-gray-500">{results.length} results</p>
          {results.map((doc) => (
            <div
              key={doc.id}
              className="rounded-lg border bg-white p-4 shadow-sm"
            >
              <div className="flex items-start justify-between">
                <div>
                  <a
                    href={doc.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="font-medium text-blue-600 hover:underline"
                  >
                    {doc.title}
                  </a>
                  <p className="mt-1 text-xs text-gray-400 truncate max-w-lg">
                    {doc.url}
                  </p>
                </div>
                <div className="flex gap-2">
                  <span className="rounded bg-gray-100 px-2 py-0.5 text-xs">
                    {doc.doc_type}
                  </span>
                  {doc.is_new && (
                    <span className="rounded bg-blue-100 px-2 py-0.5 text-xs text-blue-700">
                      New
                    </span>
                  )}
                </div>
              </div>
              {doc.first_seen_at && (
                <p className="mt-1 text-xs text-gray-400">
                  Discovered: {new Date(doc.first_seen_at).toLocaleDateString()}
                </p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
