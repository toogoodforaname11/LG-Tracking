"use client";

import { useState, useEffect } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Topics — easy to extend by adding entries here
const AVAILABLE_TOPICS = [
  { id: "ocp_updates", label: "OCP Updates" },
  { id: "rezoning_housing", label: "Rezoning / Housing" },
  { id: "environment", label: "Environment" },
  { id: "development_permits", label: "Development Permits" },
  { id: "other", label: "Other" },
] as const;

// Municipalities sourced from seed registry — Colwood first, then CRD alphabetical
const MUNICIPALITIES = [
  "Colwood",
  "Central Saanich",
  "CRD",
  "Esquimalt",
  "Highlands",
  "Langford",
  "Metchosin",
  "North Saanich",
  "Oak Bay",
  "Saanich",
  "Sidney",
  "Sooke",
  "Victoria",
  "View Royal",
];

type FormState = "idle" | "submitting" | "success" | "error";

export default function SubscribePage() {
  const [email, setEmail] = useState("");
  const [selectedMunicipalities, setSelectedMunicipalities] = useState<
    string[]
  >([]);
  const [selectedTopics, setSelectedTopics] = useState<string[]>([]);
  const [keywords, setKeywords] = useState("");
  const [formState, setFormState] = useState<FormState>("idle");
  const [errorMessage, setErrorMessage] = useState("");
  const [muniDropdownOpen, setMuniDropdownOpen] = useState(false);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      const target = e.target as HTMLElement;
      if (!target.closest("[data-muni-dropdown]")) {
        setMuniDropdownOpen(false);
      }
    };
    document.addEventListener("click", handleClickOutside);
    return () => document.removeEventListener("click", handleClickOutside);
  }, []);

  const toggleMunicipality = (name: string) => {
    setSelectedMunicipalities((prev) =>
      prev.includes(name) ? prev.filter((m) => m !== name) : [...prev, name]
    );
  };

  const toggleTopic = (id: string) => {
    setSelectedTopics((prev) =>
      prev.includes(id) ? prev.filter((t) => t !== id) : [...prev, id]
    );
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormState("submitting");
    setErrorMessage("");

    try {
      const res = await fetch(`${API_BASE}/api/v1/subscribe`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email,
          municipalities: selectedMunicipalities,
          topics: selectedTopics,
          keywords,
        }),
      });

      if (!res.ok) {
        const data = await res.json().catch(() => null);
        throw new Error(
          data?.detail || `Request failed with status ${res.status}`
        );
      }

      setFormState("success");
    } catch (err) {
      setFormState("error");
      setErrorMessage(
        err instanceof Error ? err.message : "Something went wrong"
      );
    }
  };

  if (formState === "success") {
    return (
      <div className="rounded-lg border bg-white p-8 text-center shadow-sm">
        <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-green-100">
          <svg
            className="h-8 w-8 text-green-600"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M5 13l4 4L19 7"
            />
          </svg>
        </div>
        <h2 className="mb-2 text-2xl font-bold text-gray-900">
          Preferences Saved!
        </h2>
        <p className="mb-6 text-gray-600">
          You will receive weekly digests every{" "}
          <strong>Sunday at 8 PM Pacific</strong> with AI-summarized updates
          from your selected municipalities.
        </p>
        <p className="mb-6 text-sm text-gray-500">
          A confirmation email has been sent to <strong>{email}</strong>.
        </p>
        <button
          onClick={() => setFormState("idle")}
          className="rounded-lg bg-blue-800 px-6 py-2 text-sm font-medium text-white hover:bg-blue-900"
        >
          Edit Preferences
        </button>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="rounded-lg border bg-white p-6 shadow-sm">
        <h2 className="mb-1 text-xl font-bold text-gray-900">
          Subscribe to Weekly Digests
        </h2>
        <p className="mb-6 text-sm text-gray-500">
          Get AI-summarized updates from BC municipal council meetings delivered
          to your inbox every Sunday. Enter the same email to update your
          preferences anytime.
        </p>

        {/* Email */}
        <div className="mb-5">
          <label
            htmlFor="email"
            className="mb-1 block text-sm font-medium text-gray-700"
          >
            Email Address <span className="text-red-500">*</span>
          </label>
          <input
            id="email"
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@example.com"
            className="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
          />
        </div>

        {/* Municipalities — multi-select dropdown */}
        <div className="mb-5">
          <label className="mb-1 block text-sm font-medium text-gray-700">
            Municipalities
          </label>
          <div className="relative" data-muni-dropdown>
            <button
              type="button"
              onClick={() => setMuniDropdownOpen(!muniDropdownOpen)}
              className="flex w-full items-center justify-between rounded-lg border border-gray-300 px-4 py-2.5 text-left text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
            >
              <span className="text-gray-600">
                {selectedMunicipalities.length === 0
                  ? "Select municipalities..."
                  : `${selectedMunicipalities.length} selected`}
              </span>
              <svg
                className={`h-4 w-4 text-gray-400 transition-transform ${muniDropdownOpen ? "rotate-180" : ""}`}
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            </button>

            {muniDropdownOpen && (
              <div className="absolute z-10 mt-1 max-h-60 w-full overflow-y-auto rounded-lg border border-gray-200 bg-white shadow-lg">
                {MUNICIPALITIES.map((name) => (
                  <label
                    key={name}
                    className="flex cursor-pointer items-center px-4 py-2 hover:bg-blue-50"
                  >
                    <input
                      type="checkbox"
                      checked={selectedMunicipalities.includes(name)}
                      onChange={() => toggleMunicipality(name)}
                      className="mr-3 h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                    <span className="text-sm text-gray-700">{name}</span>
                  </label>
                ))}
              </div>
            )}
          </div>

          {/* Selected pills */}
          {selectedMunicipalities.length > 0 && (
            <div className="mt-2 flex flex-wrap gap-1.5">
              {selectedMunicipalities.map((name) => (
                <span
                  key={name}
                  className="inline-flex items-center rounded-full bg-blue-100 px-2.5 py-0.5 text-xs font-medium text-blue-800"
                >
                  {name}
                  <button
                    type="button"
                    onClick={() => toggleMunicipality(name)}
                    className="ml-1 text-blue-600 hover:text-blue-900"
                  >
                    &times;
                  </button>
                </span>
              ))}
            </div>
          )}
        </div>

        {/* Topics — checkboxes */}
        <div className="mb-5">
          <label className="mb-2 block text-sm font-medium text-gray-700">
            Topics
          </label>
          <div className="grid grid-cols-2 gap-2 sm:grid-cols-3">
            {AVAILABLE_TOPICS.map((topic) => (
              <label
                key={topic.id}
                className={`flex cursor-pointer items-center rounded-lg border px-3 py-2.5 text-sm transition-colors ${
                  selectedTopics.includes(topic.id)
                    ? "border-blue-500 bg-blue-50 text-blue-800"
                    : "border-gray-200 bg-white text-gray-700 hover:bg-gray-50"
                }`}
              >
                <input
                  type="checkbox"
                  checked={selectedTopics.includes(topic.id)}
                  onChange={() => toggleTopic(topic.id)}
                  className="mr-2 h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                {topic.label}
              </label>
            ))}
          </div>
        </div>

        {/* Keywords */}
        <div className="mb-6">
          <label
            htmlFor="keywords"
            className="mb-1 block text-sm font-medium text-gray-700"
          >
            Keywords{" "}
            <span className="font-normal text-gray-400">(optional)</span>
          </label>
          <input
            id="keywords"
            type="text"
            value={keywords}
            onChange={(e) => setKeywords(e.target.value)}
            placeholder="e.g. affordable housing, bike lanes, tree bylaw"
            className="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
          />
          <p className="mt-1 text-xs text-gray-400">
            Comma-separated. We&apos;ll match these against meeting agendas and
            minutes.
          </p>
        </div>

        {/* Error */}
        {formState === "error" && (
          <div className="mb-4 rounded-lg bg-red-50 p-3 text-sm text-red-700">
            {errorMessage}
          </div>
        )}

        {/* Submit */}
        <button
          type="submit"
          disabled={formState === "submitting" || !email}
          className="w-full rounded-lg bg-blue-800 px-6 py-3 text-sm font-semibold text-white hover:bg-blue-900 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {formState === "submitting"
            ? "Saving..."
            : "Subscribe / Update Preferences"}
        </button>
      </div>

      {/* Info box */}
      <div className="rounded-lg border border-blue-100 bg-blue-50 p-4 text-sm text-blue-800">
        <p className="mb-2 font-medium">How it works:</p>
        <ul className="list-inside list-disc space-y-1 text-blue-700">
          <li>
            We scan council agendas, minutes, and meeting videos from your
            selected municipalities
          </li>
          <li>
            AI summarizes relevant items matching your topics and keywords
          </li>
          <li>
            You get one email per week (Sunday 8 PM Pacific) — no spam
          </li>
          <li>
            To change preferences, just submit this form again with the same
            email
          </li>
          <li>Every email includes a one-click unsubscribe link</li>
        </ul>
      </div>
    </form>
  );
}
