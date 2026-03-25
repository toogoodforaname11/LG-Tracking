"use client";

import { useState, useEffect } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Topics — housing, transit, and provincial priority topics
const AVAILABLE_TOPICS = [
  { id: "tod", label: "Transit Oriented Development (TOD)" },
  { id: "toa_impl", label: "Transit Oriented Areas (TOA)" },
  { id: "area_plans", label: "Area Plans (Local Area or Neighbourhood Plans)" },
  { id: "brt", label: "BRT (Bus Rapid Transit) or Bus Priority Infrastructure" },
  { id: "multimodal", label: "Multimodal Transport and Active Transportation" },
  { id: "provincial_targets", label: "Alignment with Provincial Housing Targets / Housing Needs Reports" },
  { id: "ssmuh", label: "Small-Scale Multi-Unit Housing (SSMUH) / Duplex-Triplex-Fourplex" },
  { id: "housing_statutes", label: "Housing Statutes Amendment Act / Related Bylaws" },
  { id: "ocp_housing", label: "OCP Updates" },
  { id: "zoning_density", label: "Zoning / Rezoning for Housing Density" },
  { id: "dev_permits_housing", label: "Development Permits Affecting Housing Supply" },
  { id: "dev_cost_charges", label: "Development Cost Charges or Affordability Incentives" },
  { id: "other_housing_transit", label: "Other Housing or Transit-Related Bylaws / Legislation" },
] as const;

// Keywords searched per topic — mirrors backend build_digest_items topic_keywords exactly
const TOPIC_KEYWORDS: Record<string, string[]> = {
  tod: [
    "transit-oriented development", "transit oriented development",
    "TOD", "transit hub", "transit node",
  ],
  toa_impl: [
    "transit-oriented area", "transit oriented area", "TOA",
    "Bill 47", "station area", "station precinct", "SkyTrain area",
    "frequent transit", "frequent transit network", "FTN",
    "400 metre", "400m", "800 metre", "800m",
    "bus exchange", "rapid transit station",
  ],
  area_plans: [
    "area plan", "neighbourhood plan", "local area plan",
    "community plan amendment", "area structure plan",
    "neighbourhood planning", "district plan",
  ],
  brt: [
    "bus rapid transit", "BRT", "bus priority",
    "rapid bus", "B-Line", "bus lane", "queue jump",
    "bus exchange", "transit corridor",
  ],
  multimodal: [
    "multimodal", "active transportation", "cycling infrastructure",
    "bike lane", "cycle track", "cycling network",
    "pedestrian", "walkability", "greenway", "shared path",
    "complete streets", "sidewalk improvement",
  ],
  provincial_targets: [
    "housing needs report", "housing needs assessment",
    "provincial housing target", "housing target",
    "HNR", "housing supply",
    "housing action plan", "housing strategy",
  ],
  ssmuh: [
    "small-scale multi-unit", "SSMUH", "Bill 44",
    "duplex", "triplex", "fourplex", "multiplex", "sixplex",
    "missing middle", "gentle density",
    "secondary suite", "garden suite", "carriage house",
    "infill housing", "laneway home",
  ],
  housing_statutes: [
    "housing statutes", "housing statutes amendment",
    "Bill 44", "Bill 46", "Bill 47", "Bill 16", "Bill 25",
    "provincial housing legislation", "housing legislation",
    "housing amendment", "amenity cost charge",
    "parking requirement", "development approval",
    "tenant protection", "residential infill", "as-of-right",
  ],
  ocp_housing: [
    "official community plan", "OCP", "OCP amendment",
    "community plan amendment", "land use designation",
    "future land use", "OCP bylaw", "plan amendment",
  ],
  zoning_density: [
    "rezoning", "rezone", "zoning bylaw amendment", "zoning amendment",
    "density bonus", "floor area ratio", "FAR", "floor space ratio", "FSR",
    "height increase", "density increase",
    "comprehensive development zone", "CD zone",
  ],
  dev_permits_housing: [
    "development permit", "development variance permit", "DVP",
    "building permit", "construction permit",
    "development application", "form and character",
    "amenity contribution",
  ],
  dev_cost_charges: [
    "development cost charge", "DCC", "development cost levy",
    "community amenity contribution", "CAC",
    "amenity contribution", "density bonusing",
    "affordable housing reserve", "affordability incentive",
    "waiver of fees", "fee waiver",
  ],
  other_housing_transit: [
    "housing", "affordable housing", "rental housing",
    "market rental", "below-market",
    "transit", "bus route", "SkyTrain", "rapid transit",
    "transportation plan", "mobility",
  ],
};

// BC Housing Statutes Amendment Act — specific bills the user can filter by
const HOUSING_BILLS = [
  {
    id: "bill44",
    label: "Bill 44",
    keyword: "Bill 44",
    description: "Small-Scale Multi-Unit Housing (SSMUH) — duplexes, triplexes, fourplexes as-of-right",
  },
  {
    id: "bill47",
    label: "Bill 47",
    keyword: "Bill 47",
    description: "Transit-Oriented Areas (TOA) — increased density near rapid transit stations",
  },
  {
    id: "bill16",
    label: "Bill 16 (2024)",
    keyword: "Bill 16",
    description: "Zoning bylaws, development approvals, tenant protection amendments",
  },
  {
    id: "bill25",
    label: "Bill 25 (2025)",
    keyword: "Bill 25",
    description: "SSMUH alignment, parking limit changes",
  },
] as const;

// All BC municipalities sourced from seed registry — alphabetical
const MUNICIPALITIES = [
  "100 Mile House",
  "Abbotsford",
  "Ainsworth Hot Springs",
  "Alert Bay",
  "Armstrong",
  "Ashcroft",
  "Balfour",
  "Barriere",
  "Bowen Island",
  "Burnaby",
  "Cache Creek",
  "Campbell River",
  "Canal Flats",
  "Castlegar",
  "Central Saanich",
  "Chase",
  "Chetwynd",
  "Chilliwack",
  "Christina Lake",
  "Clearwater",
  "Clinton",
  "Coldstream",
  "Colwood",
  "Comox",
  "Coquitlam",
  "Courtenay",
  "Cranbrook",
  "CRD",
  "Creston",
  "Cumberland",
  "Dawson Creek",
  "Duncan",
  "Elkford",
  "Enderby",
  "Esquimalt",
  "Fernie",
  "Fort Nelson",
  "Fort St. James",
  "Fort St. John",
  "Fruitvale",
  "Gibsons",
  "Gold River",
  "Golden",
  "Grand Forks",
  "Granisle",
  "Greenwood",
  "Harrison Hot Springs",
  "Hazelton",
  "Highlands",
  "Hope",
  "Houston",
  "Hudson's Hope",
  "Invermere",
  "Kamloops",
  "Kaslo",
  "Kelowna",
  "Kent",
  "Keremeos",
  "Kimberley",
  "Kitimat",
  "Ladysmith",
  "Lake Country",
  "Lake Cowichan",
  "Langford",
  "Langley City",
  "Langley Township",
  "Lantzville",
  "Lillooet",
  "Lions Bay",
  "Logan Lake",
  "Lumby",
  "Mackenzie",
  "Maple Ridge",
  "McBride",
  "Merritt",
  "Metchosin",
  "Midway",
  "Mission",
  "Montrose",
  "Nakusp",
  "Nanaimo",
  "Nelson",
  "New Denver",
  "New Hazelton",
  "New Westminster",
  "North Saanich",
  "North Vancouver City",
  "North Vancouver District",
  "Northern Rockies",
  "Oak Bay",
  "Oliver",
  "Osoyoos",
  "Parksville",
  "Peachland",
  "Pemberton",
  "Penticton",
  "Pitt Meadows",
  "Port Alberni",
  "Port Coquitlam",
  "Port Edward",
  "Port Hardy",
  "Port McNeill",
  "Port Moody",
  "Powell River",
  "Prince George",
  "Prince Rupert",
  "Princeton",
  "Qualicum Beach",
  "Quesnel",
  "Radium Hot Springs",
  "Revelstoke",
  "Richmond",
  "Riondel",
  "Rossland",
  "Saanich",
  "Salmo",
  "Salmon Arm",
  "Sechelt",
  "Sicamous",
  "Sidney",
  "Silverton",
  "Slocan",
  "Smithers",
  "Sooke",
  "Spallumcheen",
  "Sparwood",
  "Squamish",
  "Stewart",
  "Summerland",
  "Surrey",
  "Tahsis",
  "Telkwa",
  "Terrace",
  "Tofino",
  "Trail",
  "Tumbler Ridge",
  "Ucluelet",
  "Valemount",
  "Vancouver",
  "Vanderhoof",
  "Vernon",
  "Victoria",
  "View Royal",
  "Warfield",
  "Wells",
  "West Kelowna",
  "West Vancouver",
  "Whistler",
  "White Rock",
  "Williams Lake",
  "Zeballos",
];

type FormState = "idle" | "submitting" | "success" | "error";

export default function SubscribePage() {
  const [email, setEmail] = useState("");
  const [selectedMunicipalities, setSelectedMunicipalities] = useState<string[]>([]);
  const [selectedTopics, setSelectedTopics] = useState<string[]>([]);
  const [keywords, setKeywords] = useState("");
  const [immediateAlerts, setImmediateAlerts] = useState(true);
  const [formState, setFormState] = useState<FormState>("idle");
  const [errorMessage, setErrorMessage] = useState("");
  const [muniDropdownOpen, setMuniDropdownOpen] = useState(false);
  const [muniSearch, setMuniSearch] = useState("");
  const [expandedTopics, setExpandedTopics] = useState<Set<string>>(new Set());
  const [selectedBills, setSelectedBills] = useState<Set<string>>(new Set());

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      const target = e.target as HTMLElement;
      if (!target.closest("[data-muni-dropdown]")) {
        setMuniDropdownOpen(false);
        setMuniSearch("");
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

  const toggleExpanded = (id: string) => {
    setExpandedTopics((prev) => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  };

  const toggleBill = (billId: string) => {
    setSelectedBills((prev) => {
      const next = new Set(prev);
      if (next.has(billId)) {
        next.delete(billId);
      } else {
        next.add(billId);
      }
      return next;
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormState("submitting");
    setErrorMessage("");

    try {
      // Merge any specifically-checked bills into the keywords string
      const billKeywords = HOUSING_BILLS
        .filter((b) => selectedBills.has(b.id))
        .map((b) => b.keyword);
      const allKeywords = [keywords, ...billKeywords]
        .map((k) => k.trim())
        .filter(Boolean)
        .join(", ");

      const res = await fetch(`${API_BASE}/api/v1/subscribe`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email,
          municipalities: selectedMunicipalities,
          topics: selectedTopics,
          keywords: allKeywords,
          immediate_alerts: immediateAlerts,
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
        <p className="mb-4 text-gray-600">
          You will receive{" "}
          {immediateAlerts ? (
            <>
              <strong>immediate alerts</strong> (if enabled) +{" "}
            </>
          ) : null}
          <strong>weekly digests every Sunday</strong>. Re-visit this page
          anytime to edit.
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
          BC Local Government Watch &mdash; Housing, Transit &amp; Provincial
          Priority Updates
        </h2>
        <p className="mb-6 text-sm text-gray-500">
          Subscribe to updates on housing, transit, and local government
          hearings. Enter the same email to update your preferences anytime.
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

        {/* Keywords / Bylaw / Bill Tracking — MOST PROMINENT FIELD */}
        <div className="mb-6 rounded-xl border-2 border-blue-500 bg-blue-50 p-5 shadow-md">
          <label
            htmlFor="keywords"
            className="mb-2 block text-lg font-bold text-blue-900"
          >
            Track Specific Bills, Bylaws, or Keywords
          </label>
          <input
            id="keywords"
            type="text"
            value={keywords}
            onChange={(e) => setKeywords(e.target.value)}
            placeholder="e.g. Bylaw 1700, Bill 44, TOA zoning, affordable housing"
            className="w-full rounded-lg border-2 border-blue-400 bg-white px-4 py-3 text-base focus:border-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-300"
          />
          <div className="mt-3 rounded-lg border border-blue-200 bg-white px-4 py-3 text-sm leading-relaxed text-blue-800">
            Enter specific bylaw numbers, bill names, or keywords you want to
            track (e.g. &lsquo;Bylaw 1700&rsquo;, &lsquo;Housing Statutes
            Amendment Act&rsquo;, &lsquo;TOA zoning&rsquo;, &lsquo;TOD area
            plan&rsquo;). The system will alert you every time these exact terms
            are mentioned in any hearing.
          </div>
          <p className="mt-2 text-xs text-blue-600">
            Comma-separated. We&apos;ll match these against meeting agendas,
            minutes, and videos.
          </p>
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
              <div className="absolute z-10 mt-1 max-h-72 w-full overflow-hidden rounded-lg border border-gray-200 bg-white shadow-lg">
                <div className="sticky top-0 border-b border-gray-100 bg-white p-2">
                  <input
                    type="text"
                    value={muniSearch}
                    onChange={(e) => setMuniSearch(e.target.value)}
                    placeholder="Search municipalities..."
                    className="w-full rounded border border-gray-200 px-3 py-1.5 text-sm focus:border-blue-400 focus:outline-none"
                    onClick={(e) => e.stopPropagation()}
                  />
                </div>
                <div className="max-h-60 overflow-y-auto">
                {MUNICIPALITIES.filter((name) =>
                  name.toLowerCase().includes(muniSearch.toLowerCase())
                ).map((name) => (
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

        {/* Topics — checkboxes with expandable keyword list */}
        <div className="mb-5">
          <label className="mb-2 block text-sm font-medium text-gray-700">
            Topics
          </label>
          <p className="mb-3 text-xs text-gray-500">
            Tap the arrow on any topic to see the keywords it searches for.
          </p>
          <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
            {AVAILABLE_TOPICS.map((topic) => {
              const isSelected = selectedTopics.includes(topic.id);
              const isExpanded = expandedTopics.has(topic.id);
              const kws = TOPIC_KEYWORDS[topic.id] ?? [];

              return (
                <div
                  key={topic.id}
                  className={`rounded-lg border text-sm transition-colors ${
                    isSelected
                      ? "border-blue-500 bg-blue-50"
                      : "border-gray-200 bg-white"
                  }`}
                >
                  {/* Top row: checkbox + label + chevron */}
                  <div className="flex items-center">
                    {/* Checkbox area — clicking this toggles selection */}
                    <label className="flex flex-1 cursor-pointer items-center gap-2 px-3 py-2.5">
                      <input
                        type="checkbox"
                        checked={isSelected}
                        onChange={() => toggleTopic(topic.id)}
                        className="h-4 w-4 shrink-0 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      />
                      <span className={isSelected ? "text-blue-800" : "text-gray-700"}>
                        {topic.label}
                      </span>
                    </label>

                    {/* Chevron — clicking this toggles keyword expansion only */}
                    <button
                      type="button"
                      onClick={() => toggleExpanded(topic.id)}
                      aria-label={isExpanded ? "Hide search terms" : "Show search terms"}
                      className={`flex h-full shrink-0 items-center px-3 py-2.5 transition-colors ${
                        isExpanded
                          ? "text-blue-600"
                          : "text-gray-400 hover:text-gray-600"
                      }`}
                    >
                      <svg
                        className={`h-4 w-4 transition-transform duration-200 ${isExpanded ? "rotate-180" : ""}`}
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
                  </div>

                  {/* Expanded section */}
                  {isExpanded && topic.id === "housing_statutes" ? (
                    <div className="border-t border-gray-100 px-3 pb-3 pt-2">
                      <p className="mb-2 text-xs font-medium text-gray-500">
                        Filter by specific bill (leave all unchecked to match any):
                      </p>
                      <div className="space-y-1.5">
                        {HOUSING_BILLS.map((bill) => (
                          <label
                            key={bill.id}
                            className="flex cursor-pointer items-start gap-2"
                          >
                            <input
                              type="checkbox"
                              checked={selectedBills.has(bill.id)}
                              onChange={() => toggleBill(bill.id)}
                              className="mt-0.5 h-4 w-4 shrink-0 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                            />
                            <span className="text-xs text-gray-700">
                              <span className="font-semibold">{bill.label}</span>
                              {" — "}
                              {bill.description}
                            </span>
                          </label>
                        ))}
                      </div>
                    </div>
                  ) : isExpanded && kws.length > 0 ? (
                    <div className="border-t border-gray-100 px-3 pb-3 pt-2">
                      <p className="mb-1.5 text-xs font-medium text-gray-500">
                        Searches for:
                      </p>
                      <div className="flex flex-wrap gap-1">
                        {kws.map((kw) => (
                          <span
                            key={kw}
                            className="rounded-full bg-gray-100 px-2 py-0.5 text-xs text-gray-600"
                          >
                            {kw}
                          </span>
                        ))}
                      </div>
                    </div>
                  ) : null}
                </div>
              );
            })}
          </div>
        </div>

        {/* Immediate Alerts checkbox */}
        <div className="mb-6 rounded-lg border border-amber-200 bg-amber-50 p-4">
          <label className="flex cursor-pointer items-start gap-3">
            <input
              type="checkbox"
              checked={immediateAlerts}
              onChange={(e) => setImmediateAlerts(e.target.checked)}
              className="mt-0.5 h-4 w-4 rounded border-gray-300 text-amber-600 focus:ring-amber-500"
            />
            <div>
              <span className="text-sm font-medium text-amber-900">
                Send me immediate alerts after each matching council meeting
              </span>
              <p className="mt-1 text-xs text-amber-700">
                We poll sources every 30 minutes. When a new matching item is
                detected, you&apos;ll receive an email right away. Weekly
                digests are always sent regardless of this setting.
              </p>
            </div>
          </label>
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
            : "Subscribe / Update My Preferences"}
        </button>
      </div>

      {/* Info box */}
      <div className="rounded-lg border border-blue-100 bg-blue-50 p-4 text-sm text-blue-800">
        <p className="mb-2 font-medium">How it works:</p>
        <ul className="list-inside list-disc space-y-1 text-blue-700">
          <li>
            We scan council agendas, minutes, and meeting videos from your
            selected municipalities every 30 minutes
          </li>
          <li>
            AI summarizes relevant items matching your topics and keywords
          </li>
          <li>
            <strong>Immediate alerts</strong> (default ON): get emailed within
            minutes when a new matching item appears
          </li>
          <li>
            <strong>Weekly digest</strong> (always): full summary every Sunday
            at 8 PM Pacific
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
