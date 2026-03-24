"use client";

import { useEffect, useState } from "react";
import { getMunicipalities, seedRegistry } from "@/lib/api";
import type { Municipality } from "@/lib/api";

const PLATFORM_COLORS: Record<string, string> = {
  civicweb: "bg-green-100 text-green-800",
  youtube: "bg-red-100 text-red-800",
  granicus: "bg-purple-100 text-purple-800",
  custom: "bg-gray-100 text-gray-800",
  unknown: "bg-yellow-100 text-yellow-800",
};

export default function MunicipalitiesPage() {
  const [municipalities, setMunicipalities] = useState<Municipality[]>([]);
  const [loading, setLoading] = useState(true);
  const [seeding, setSeeding] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    try {
      const data = await getMunicipalities();
      setMunicipalities(data.municipalities);
    } catch {
      setError("Failed to load municipalities. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const handleSeed = async () => {
    setSeeding(true);
    try {
      const result = await seedRegistry();
      alert(
        `Seeded: ${result.municipalities_created} new municipalities, ${result.sources_created} new sources`
      );
      await load();
    } catch {
      setError("Failed to seed registry");
    } finally {
      setSeeding(false);
    }
  };

  if (loading) return <p className="text-gray-500">Loading...</p>;

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <h2 className="text-2xl font-bold">Municipalities</h2>
        <button
          onClick={handleSeed}
          disabled={seeding}
          className="rounded-lg border px-4 py-2 text-sm font-medium hover:bg-gray-50 disabled:opacity-50"
        >
          {seeding ? "Seeding..." : "Seed CRD Registry"}
        </button>
      </div>

      {error && (
        <div className="mb-4 rounded-lg bg-red-50 p-4 text-sm text-red-700">{error}</div>
      )}

      {municipalities.length === 0 ? (
        <div className="rounded-lg border-2 border-dashed p-8 text-center text-gray-500">
          <p className="mb-2">No municipalities loaded yet.</p>
          <button
            onClick={handleSeed}
            className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
          >
            Seed CRD Registry
          </button>
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {municipalities.map((m) => (
            <div key={m.id} className="rounded-lg border bg-white p-4 shadow-sm">
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="font-semibold">{m.short_name}</h3>
                  <p className="text-xs text-gray-500">{m.name}</p>
                </div>
                <span className="rounded bg-gray-100 px-2 py-0.5 text-xs">
                  {m.gov_type}
                </span>
              </div>

              {m.population && (
                <p className="mt-1 text-xs text-gray-400">
                  Pop: {m.population.toLocaleString()}
                </p>
              )}

              {m.website_url && (
                <a
                  href={m.website_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="mt-1 block text-xs text-blue-600 hover:underline truncate"
                >
                  {m.website_url}
                </a>
              )}

              <div className="mt-3 flex flex-wrap gap-1">
                {m.sources.map((s) => (
                  <span
                    key={s.id}
                    className={`rounded-full px-2 py-0.5 text-xs ${
                      PLATFORM_COLORS[s.platform] || PLATFORM_COLORS.unknown
                    }`}
                    title={s.label}
                  >
                    {s.platform} ({s.source_type})
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
