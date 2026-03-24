"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  getMunicipalities,
  getTracks,
  getTrackMatches,
  triggerPoll,
  triggerProcessing,
  deleteTrack,
} from "@/lib/api";
import type { Municipality, Track, TrackMatch } from "@/lib/api";

export default function Home() {
  const [municipalities, setMunicipalities] = useState<Municipality[]>([]);
  const [tracks, setTracks] = useState<Track[]>([]);
  const [matches, setMatches] = useState<Record<number, TrackMatch[]>>({});
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    try {
      const [muniData, tracksData] = await Promise.all([
        getMunicipalities(),
        getTracks(),
      ]);
      setMunicipalities(muniData.municipalities);
      setTracks(tracksData);

      // Load matches for each track
      const matchesMap: Record<number, TrackMatch[]> = {};
      for (const track of tracksData) {
        try {
          matchesMap[track.id] = await getTrackMatches(track.id);
        } catch {
          matchesMap[track.id] = [];
        }
      }
      setMatches(matchesMap);
    } catch {
      setError("Failed to load data. Is the backend running on localhost:8000?");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const handlePoll = async () => {
    setRunning("poll");
    try {
      await triggerPoll();
      await load();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Poll failed");
    } finally {
      setRunning(null);
    }
  };

  const handleProcess = async () => {
    setRunning("process");
    try {
      await triggerProcessing();
      await load();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Processing failed");
    } finally {
      setRunning(null);
    }
  };

  const handleRunAll = async () => {
    setRunning("all");
    try {
      await triggerPoll();
      await triggerProcessing();
      await load();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Pipeline failed");
    } finally {
      setRunning(null);
    }
  };

  const handleDeleteTrack = async (id: number) => {
    try {
      await deleteTrack(id);
      await load();
    } catch {
      setError("Failed to delete track");
    }
  };

  const muniMap = Object.fromEntries(municipalities.map((m) => [m.id, m]));
  const activeSources = municipalities.reduce(
    (acc, m) => acc + m.sources.filter((s) => s.scrape_status === "active").length,
    0
  );

  if (loading) return <p className="text-gray-500">Loading...</p>;

  return (
    <div className="space-y-8">
      {error && (
        <div className="rounded-lg bg-red-50 p-4 text-sm text-red-700">
          {error}
          <button onClick={() => setError(null)} className="ml-2 font-medium underline">
            Dismiss
          </button>
        </div>
      )}

      <section>
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-bold">Dashboard</h2>
          <span className="text-xs text-gray-400">
            demo user: demo-gov001
          </span>
        </div>
        <p className="mt-1 text-gray-600">
          Track BC local government hearing updates. Opt-in to topics and get alerts.
        </p>
      </section>

      {/* Stats */}
      <section className="grid gap-4 sm:grid-cols-4">
        <div className="rounded-lg border bg-white p-5 shadow-sm">
          <h3 className="text-sm font-medium text-gray-500">Municipalities</h3>
          <p className="mt-1 text-3xl font-bold">{municipalities.length}</p>
          <p className="text-sm text-gray-400">CRD region</p>
        </div>
        <div className="rounded-lg border bg-white p-5 shadow-sm">
          <h3 className="text-sm font-medium text-gray-500">Active Sources</h3>
          <p className="mt-1 text-3xl font-bold">{activeSources}</p>
          <p className="text-sm text-gray-400">CivicWeb + YouTube</p>
        </div>
        <div className="rounded-lg border bg-white p-5 shadow-sm">
          <h3 className="text-sm font-medium text-gray-500">Your Tracks</h3>
          <p className="mt-1 text-3xl font-bold">
            {tracks.filter((t) => t.is_active).length}
          </p>
          <p className="text-sm text-gray-400">active</p>
        </div>
        <div className="rounded-lg border bg-white p-5 shadow-sm">
          <h3 className="text-sm font-medium text-gray-500">Matches</h3>
          <p className="mt-1 text-3xl font-bold">
            {Object.values(matches).reduce((a, m) => a + m.length, 0)}
          </p>
          <p className="text-sm text-gray-400">total</p>
        </div>
      </section>

      {/* Actions */}
      <section>
        <h3 className="mb-3 text-lg font-semibold">Actions</h3>
        <div className="flex flex-wrap gap-3">
          <Link
            href="/tracks/new"
            className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
          >
            Create Track
          </Link>
          <Link
            href="/municipalities"
            className="rounded-lg border px-4 py-2 text-sm font-medium hover:bg-gray-50"
          >
            Browse Municipalities
          </Link>
          <Link
            href="/search"
            className="rounded-lg border px-4 py-2 text-sm font-medium hover:bg-gray-50"
          >
            Search
          </Link>
          <button
            onClick={handlePoll}
            disabled={!!running}
            className="rounded-lg border border-green-200 bg-green-50 px-4 py-2 text-sm font-medium text-green-700 hover:bg-green-100 disabled:opacity-50"
          >
            {running === "poll" ? "Polling..." : "Poll Sources"}
          </button>
          <button
            onClick={handleProcess}
            disabled={!!running}
            className="rounded-lg border border-purple-200 bg-purple-50 px-4 py-2 text-sm font-medium text-purple-700 hover:bg-purple-100 disabled:opacity-50"
          >
            {running === "process" ? "Processing..." : "Process Matches"}
          </button>
          <button
            onClick={handleRunAll}
            disabled={!!running}
            className="rounded-lg border border-amber-200 bg-amber-50 px-4 py-2 text-sm font-medium text-amber-700 hover:bg-amber-100 disabled:opacity-50"
          >
            {running === "all" ? "Running..." : "Run Full Pipeline"}
          </button>
        </div>
      </section>

      {/* Tracks */}
      <section>
        <h3 className="mb-3 text-lg font-semibold">My Tracks</h3>
        {tracks.length === 0 ? (
          <div className="rounded-lg border-2 border-dashed p-6 text-center text-gray-500">
            <p>No tracks yet.</p>
            <Link
              href="/tracks/new"
              className="mt-2 inline-block text-blue-600 hover:underline"
            >
              Create your first track
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            {tracks.map((track) => (
              <div
                key={track.id}
                className={`rounded-lg border bg-white p-4 shadow-sm ${
                  !track.is_active ? "opacity-50" : ""
                }`}
              >
                <div className="flex items-start justify-between">
                  <div>
                    <h4 className="font-semibold">{track.name}</h4>
                    <p className="text-sm text-gray-500">
                      {track.municipality_ids
                        .map((id) => muniMap[id]?.short_name || `#${id}`)
                        .join(", ")}
                    </p>
                  </div>
                  <div className="flex items-center gap-2">
                    <span
                      className={`rounded-full px-2 py-0.5 text-xs ${
                        track.is_active
                          ? "bg-green-100 text-green-700"
                          : "bg-gray-100 text-gray-500"
                      }`}
                    >
                      {track.is_active ? "Active" : "Inactive"}
                    </span>
                    <button
                      onClick={() => handleDeleteTrack(track.id)}
                      className="text-xs text-red-500 hover:underline"
                    >
                      Deactivate
                    </button>
                  </div>
                </div>

                <div className="mt-2 flex flex-wrap gap-1">
                  {track.topics.map((t) => (
                    <span
                      key={t}
                      className="rounded-full bg-blue-50 px-2 py-0.5 text-xs text-blue-700"
                    >
                      {t}
                    </span>
                  ))}
                  {track.keywords.map((k) => (
                    <span
                      key={k}
                      className="rounded-full bg-amber-50 px-2 py-0.5 text-xs text-amber-700"
                    >
                      {k}
                    </span>
                  ))}
                </div>

                {/* Matches for this track */}
                {(matches[track.id] || []).length > 0 && (
                  <div className="mt-3 border-t pt-3">
                    <p className="mb-2 text-xs font-medium text-gray-500">
                      {matches[track.id].length} matches
                    </p>
                    {matches[track.id].slice(0, 3).map((m) => (
                      <div key={m.id} className="mb-2 rounded bg-gray-50 p-2 text-sm">
                        <div className="flex items-center gap-2">
                          <span
                            className={`rounded px-1.5 py-0.5 text-xs ${
                              m.verification_status === "verified"
                                ? "bg-green-100 text-green-700"
                                : "bg-yellow-100 text-yellow-700"
                            }`}
                          >
                            {m.verification_status || "unverified"}
                          </span>
                          <span className="text-xs text-gray-400">
                            {m.match_score != null
                              ? `${(m.match_score * 100).toFixed(0)}% match`
                              : ""}
                          </span>
                        </div>
                        {m.summary && (
                          <p className="mt-1 text-xs text-gray-600 line-clamp-2">
                            {m.summary}
                          </p>
                        )}
                        {m.match_reason && !m.summary && (
                          <p className="mt-1 text-xs text-gray-500">{m.match_reason}</p>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </section>

      <footer className="mt-12 border-t pt-4 text-xs text-gray-400">
        <p>
          Public data only. Not official government communication. AI-generated
          summaries may contain errors — always verify with original sources.
        </p>
      </footer>
    </div>
  );
}
