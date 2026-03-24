"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getMunicipalities, createTrack, getTopics } from "@/lib/api";
import type { Municipality } from "@/lib/api";

const TOPIC_LABELS: Record<string, string> = {
  ocp_updates: "OCP Updates",
  rezoning: "Rezoning",
  development_permits: "Development Permits",
  public_hearings: "Public Hearings",
  bylaws: "Bylaws",
  budget: "Budget",
  environment: "Environment",
  transportation: "Transportation",
  housing: "Housing",
  parks_recreation: "Parks & Recreation",
  utilities: "Utilities",
  governance: "Governance",
};

export default function NewTrackPage() {
  const router = useRouter();
  const [municipalities, setMunicipalities] = useState<Municipality[]>([]);
  const [availableTopics, setAvailableTopics] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Form state
  const [name, setName] = useState("");
  const [selectedMunis, setSelectedMunis] = useState<number[]>([]);
  const [selectedTopics, setSelectedTopics] = useState<string[]>([]);
  const [keywords, setKeywords] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const [muniData, topicData] = await Promise.all([
          getMunicipalities(),
          getTopics(),
        ]);
        setMunicipalities(muniData.municipalities);
        setAvailableTopics(topicData.topics);
      } catch (e) {
        setError("Failed to load data. Is the backend running?");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const toggleMuni = (id: number) => {
    setSelectedMunis((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    );
  };

  const toggleTopic = (topic: string) => {
    setSelectedTopics((prev) =>
      prev.includes(topic) ? prev.filter((x) => x !== topic) : [...prev, topic]
    );
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim() || selectedMunis.length === 0) {
      setError("Please provide a name and select at least one municipality.");
      return;
    }

    setSubmitting(true);
    setError(null);
    try {
      await createTrack({
        name: name.trim(),
        municipality_ids: selectedMunis,
        topics: selectedTopics,
        keywords: keywords
          .split(",")
          .map((k) => k.trim())
          .filter(Boolean),
      });
      router.push("/");
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Failed to create track");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return <p className="text-gray-500">Loading...</p>;
  }

  return (
    <div className="max-w-2xl">
      <h2 className="mb-6 text-2xl font-bold">Create New Track</h2>

      {error && (
        <div className="mb-4 rounded-lg bg-red-50 p-4 text-sm text-red-700">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Track Name */}
        <div>
          <label className="mb-1 block text-sm font-medium">Track Name</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="e.g., Colwood OCP Updates"
            className="w-full rounded-lg border px-3 py-2 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
          />
        </div>

        {/* Municipalities */}
        <div>
          <label className="mb-2 block text-sm font-medium">
            Municipalities ({selectedMunis.length} selected)
          </label>
          <div className="grid grid-cols-2 gap-2 rounded-lg border p-3 max-h-64 overflow-y-auto">
            {municipalities.map((m) => (
              <label
                key={m.id}
                className={`flex cursor-pointer items-center gap-2 rounded px-2 py-1 text-sm hover:bg-gray-50 ${
                  selectedMunis.includes(m.id) ? "bg-blue-50 font-medium" : ""
                }`}
              >
                <input
                  type="checkbox"
                  checked={selectedMunis.includes(m.id)}
                  onChange={() => toggleMuni(m.id)}
                  className="rounded"
                />
                {m.short_name}
                <span className="text-xs text-gray-400">
                  {m.sources.length > 0 ? `(${m.sources.length} sources)` : ""}
                </span>
              </label>
            ))}
          </div>
        </div>

        {/* Topics */}
        <div>
          <label className="mb-2 block text-sm font-medium">
            Topics ({selectedTopics.length} selected)
          </label>
          <div className="flex flex-wrap gap-2">
            {availableTopics.map((topic) => (
              <button
                key={topic}
                type="button"
                onClick={() => toggleTopic(topic)}
                className={`rounded-full border px-3 py-1 text-sm transition ${
                  selectedTopics.includes(topic)
                    ? "border-blue-500 bg-blue-50 text-blue-700"
                    : "border-gray-200 hover:border-gray-300"
                }`}
              >
                {TOPIC_LABELS[topic] || topic}
              </button>
            ))}
          </div>
        </div>

        {/* Keywords */}
        <div>
          <label className="mb-1 block text-sm font-medium">
            Keywords (comma-separated)
          </label>
          <input
            type="text"
            value={keywords}
            onChange={(e) => setKeywords(e.target.value)}
            placeholder="e.g., OCP, affordable housing, climate action"
            className="w-full rounded-lg border px-3 py-2 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
          />
          <p className="mt-1 text-xs text-gray-400">
            Documents containing these keywords will be flagged for your review.
          </p>
        </div>

        {/* Submit */}
        <div className="flex gap-3">
          <button
            type="submit"
            disabled={submitting}
            className="rounded-lg bg-blue-600 px-6 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
          >
            {submitting ? "Creating..." : "Create Track"}
          </button>
          <button
            type="button"
            onClick={() => router.push("/")}
            className="rounded-lg border px-6 py-2 text-sm font-medium hover:bg-gray-50"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}
