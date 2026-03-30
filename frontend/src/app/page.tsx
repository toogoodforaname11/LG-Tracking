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
  { id: "transportation_plan", label: "Transportation Plan or Transportation Study" },
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
    "bus exchange", "transit corridor", "rapid transit",
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
  transportation_plan: [
    "transportation plan", "transportation study",
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

// Fallback municipality list used when the API is unreachable.
const FALLBACK_MUNICIPALITIES = [
  "100 Mile House",
  "Abbotsford",
  "Ainsworth Hot Springs",
  "Alert Bay",
  "Anmore",
  "Armstrong",
  "Ashcroft",
  "Balfour",
  "Barriere",
  "Belcarra",
  "Bowen Island",
  "Burnaby",
  "Burns Lake",
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
  "Delta",
  "Duncan",
  "Elkford",
  "Enderby",
  "Esquimalt",
  "Fernie",
  "Fort Nelson",
  "Fort St. James",
  "Fort St. John",
  "Fraser Lake",
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
  "Lytton",
  "Mackenzie",
  "Maple Ridge",
  "Masset",
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
  "North Cowichan",
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
  "Port Alice",
  "Port Clements",
  "Port Coquitlam",
  "Port Edward",
  "Port Hardy",
  "Port McNeill",
  "Port Moody",
  "Pouce Coupe",
  "Powell River",
  "Prince George",
  "Prince Rupert",
  "Princeton",
  "Qualicum Beach",
  "Queen Charlotte",
  "Quesnel",
  "Radium Hot Springs",
  "Revelstoke",
  "Richmond",
  "Riondel",
  "Rossland",
  "Saanich",
  "Salmo",
  "Salmon Arm",
  "Sayward",
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
  "Sun Peaks",
  "Surrey",
  "Tahsis",
  "Taylor",
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

type FormState = "idle" | "submitting" | "success" | "magic_link_sent" | "confirmed" | "error";

export default function SubscribePage() {
  const [email, setEmail] = useState("");
  const [municipalities, setMunicipalities] = useState<string[]>(FALLBACK_MUNICIPALITIES);
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

  // Show "confirmed" state when redirected back from a magic link click.
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    if (params.get("confirmed") === "true") {
      setFormState("confirmed");
      // Clean the query param from the URL without a page reload.
      window.history.replaceState({}, "", window.location.pathname);
    }
  }, []);

  // Fetch municipality list from API (falls back to hardcoded list on error)
  useEffect(() => {
    fetch(`${API_BASE}/api/v1/municipalities`)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((data: { municipalities: { short_name: string }[] }) => {
        const names = data.municipalities.map((m) => m.short_name).sort();
        if (names.length > 0) setMunicipalities(names);
      })
      .catch(() => {
        // Silently fall back to FALLBACK_MUNICIPALITIES (already set as default)
      });
  }, []);

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

      const data = await res.json();
      if (data.status === "magic_link_sent") {
        setFormState("magic_link_sent");
      } else {
        setFormState("success");
      }
    } catch (err) {
      setFormState("error");
      setErrorMessage(
        err instanceof Error ? err.message : "Something went wrong"
      );
    }
  };

  if (formState === "success") {
    return (
      <div className="rounded-lg border border-gray-200 bg-white p-8 shadow-sm">
        <div className="text-center">
          <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-green-100">
            <svg className="h-7 w-7 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h2 className="mb-2 text-xl font-bold text-gray-900">Preferences Saved</h2>
          <p className="mb-6 text-sm text-gray-500">
            Confirmation sent to <strong className="text-gray-700">{email}</strong>
          </p>
        </div>

        <div className="mb-6 space-y-2">
          <div className="flex items-center gap-3 rounded-lg border border-gray-100 bg-gray-50 px-4 py-3">
            <svg className="h-4 w-4 shrink-0 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <span className="text-sm text-gray-700">Weekly digest every Sunday at 8 PM Pacific</span>
          </div>
          {immediateAlerts && (
            <div className="flex items-center gap-3 rounded-lg border border-gray-100 bg-gray-50 px-4 py-3">
              <svg className="h-4 w-4 shrink-0 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              <span className="text-sm text-gray-700">Immediate alerts enabled</span>
            </div>
          )}
        </div>

        <button
          onClick={() => setFormState("idle")}
          className="flex w-full items-center justify-center gap-2 rounded-lg border border-gray-300 px-6 py-2.5 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-50"
        >
          <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
          Edit Preferences
        </button>
      </div>
    );
  }

  if (formState === "magic_link_sent") {
    return (
      <div className="rounded-lg border border-gray-200 bg-white p-8 shadow-sm">
        <div className="text-center">
          <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-blue-100">
            <svg className="h-7 w-7 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
          <h2 className="mb-2 text-xl font-bold text-gray-900">Check Your Inbox</h2>
          <p className="mb-4 text-sm text-gray-600">
            A confirmation link has been sent to <strong className="text-gray-800">{email}</strong>.
            Click it to apply your updated preferences.
          </p>
        </div>

        <div className="mb-6 flex items-start gap-2.5 rounded-lg border border-gray-100 bg-gray-50 p-3">
          <svg className="mt-0.5 h-4 w-4 shrink-0 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p className="text-xs text-gray-500">
            The link expires in 24 hours. If you did not request this change, you can safely ignore the email.
          </p>
        </div>

        <button
          onClick={() => setFormState("idle")}
          className="flex w-full items-center justify-center gap-2 rounded-lg border border-gray-300 px-6 py-2.5 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-50"
        >
          <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Back
        </button>
      </div>
    );
  }

  if (formState === "confirmed") {
    return (
      <div className="rounded-lg border border-gray-200 bg-white p-8 shadow-sm">
        <div className="text-center">
          <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-green-100">
            <svg className="h-7 w-7 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          </div>
          <h2 className="mb-2 text-xl font-bold text-gray-900">Preferences Confirmed</h2>
          <p className="mb-6 text-sm text-gray-500">
            Your subscription preferences have been verified and saved.
          </p>
        </div>
        <button
          onClick={() => setFormState("idle")}
          className="flex w-full items-center justify-center gap-2 rounded-lg border border-gray-300 px-6 py-2.5 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-50"
        >
          <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
          Edit Preferences
        </button>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      {/* ── Main form card ── */}
      <div className="rounded-lg border border-gray-200 bg-white shadow-sm">

        {/* Email */}
        <div className="p-5">
          <label htmlFor="email" className="mb-3 block text-sm font-semibold text-gray-900">
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
          <p className="mt-1.5 text-xs text-gray-400">
            Already subscribed? Enter the same email to update your preferences.
          </p>
        </div>

        {/* Custom Keywords */}
        <div className="border-t border-gray-100 p-5">
          <h2 className="mb-1 text-sm font-semibold text-gray-900">
            Custom Keywords
          </h2>
          <p className="mb-3 text-xs text-gray-500">
            Track specific bylaw numbers, bill names, or phrases. You&apos;ll be notified every time these exact terms appear in council documents.
          </p>
          <input
            id="keywords"
            type="text"
            value={keywords}
            onChange={(e) => setKeywords(e.target.value)}
            placeholder="e.g. Bylaw 1700, Bill 44, TOA zoning, affordable housing"
            className="w-full rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
          />
          <p className="mt-1.5 text-xs text-gray-400">
            Comma-separated. Matched against agendas, minutes, and videos.
          </p>
        </div>

        {/* Municipalities */}
        <div className="border-t border-gray-100 p-5">
          <h2 className="mb-3 text-sm font-semibold text-gray-900">
            Municipalities <span className="font-normal text-gray-400">(optional)</span>
          </h2>
          <div className="relative" data-muni-dropdown>
            <button
              type="button"
              onClick={() => setMuniDropdownOpen(!muniDropdownOpen)}
              className="flex w-full items-center justify-between rounded-lg border border-gray-300 px-4 py-2.5 text-left text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
            >
              <span className="text-gray-500">
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
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            {muniDropdownOpen && (
              <div className="absolute z-10 mt-1 max-h-72 w-full overflow-hidden rounded-lg border border-gray-200 bg-white shadow-lg">
                <div className="sticky top-0 border-b border-gray-100 bg-white p-2">
                  <input
                    type="text"
                    value={muniSearch}
                    onChange={(e) => setMuniSearch(e.target.value)}
                    placeholder="Type to filter..."
                    className="w-full rounded border border-gray-200 px-3 py-1.5 text-sm focus:border-blue-400 focus:outline-none"
                    onClick={(e) => e.stopPropagation()}
                    autoFocus
                  />
                </div>
                <div className="max-h-60 overflow-y-auto">
                  {municipalities.filter((name) =>
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
            <div className="mt-2.5">
              <div className="mb-1.5 flex items-center justify-between">
                <span className="text-xs text-gray-400">{selectedMunicipalities.length} selected</span>
                <button
                  type="button"
                  onClick={() => setSelectedMunicipalities([])}
                  className="text-xs text-gray-400 hover:text-red-500"
                >
                  Clear all
                </button>
              </div>
              <div className="flex flex-wrap gap-1.5">
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
            </div>
          )}
        </div>

        {/* Topics — collapsible */}
        <details className="group border-t border-gray-100">
          <summary className="flex cursor-pointer items-center gap-2 p-5 text-sm font-semibold text-gray-900 hover:text-gray-700">
            <svg className="h-4 w-4 text-gray-400 transition-transform group-open:rotate-90" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
            Sample Topics <span className="font-normal text-gray-400">(optional)</span>
          </summary>
          <div className="grid grid-cols-1 gap-2 px-5 pb-5 sm:grid-cols-2">
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
                      : "border-gray-200 bg-white hover:border-gray-300"
                  }`}
                >
                  {/* Top row: checkbox + label + keyword toggle */}
                  <div className="flex items-center">
                    <label className="flex min-w-0 flex-1 cursor-pointer items-center gap-2 px-3 py-2.5">
                      <input
                        type="checkbox"
                        checked={isSelected}
                        onChange={() => toggleTopic(topic.id)}
                        className="h-4 w-4 shrink-0 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      />
                      <span className={`${isSelected ? "font-medium text-blue-800" : "text-gray-700"}`}>
                        {topic.label}
                      </span>
                    </label>

                    <button
                      type="button"
                      onClick={() => toggleExpanded(topic.id)}
                      aria-label={isExpanded ? "Hide search terms" : "Show search terms"}
                      className={`flex shrink-0 items-center gap-1 border-l border-gray-100 px-2.5 py-2.5 text-xs transition-colors ${
                        isExpanded
                          ? "font-medium text-blue-600"
                          : "text-gray-400 hover:text-gray-600"
                      }`}
                    >
                      <span className="hidden sm:inline">keywords</span>
                      <svg
                        className={`h-3 w-3 transition-transform duration-200 ${isExpanded ? "rotate-180" : ""}`}
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
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
                              {" -- "}
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
        </details>

      </div>

      {/* ── Delivery + Submit card ── */}
      <div className="rounded-lg border border-gray-200 bg-white p-5 shadow-sm">
        <label className="flex cursor-pointer items-start gap-3">
          <input
            type="checkbox"
            checked={immediateAlerts}
            onChange={(e) => setImmediateAlerts(e.target.checked)}
            className="mt-0.5 h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
          />
          <div>
            <span className="text-sm font-medium text-gray-900">Send immediate alerts</span>
            <p className="mt-0.5 text-xs text-gray-500">
              Get emailed within minutes when a new matching item is detected. Sources are polled every 30 minutes.
            </p>
          </div>
        </label>
        <p className="mt-3 text-xs text-gray-400">
          Weekly digests are sent every Sunday at 8 PM Pacific regardless of this setting.
        </p>

        {/* Error */}
        {formState === "error" && (
          <div className="mt-4 flex items-center gap-2.5 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">
            <svg className="h-4 w-4 shrink-0 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {errorMessage}
          </div>
        )}

        <p className="mt-4 text-center text-xs text-gray-400">
          Every email includes a one-click unsubscribe link.
        </p>

        <button
          type="submit"
          disabled={formState === "submitting" || !email}
          className="mt-3 flex w-full items-center justify-center gap-2 rounded-lg bg-blue-800 px-6 py-3 text-sm font-semibold text-white transition-colors hover:bg-blue-900 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {formState === "submitting" ? (
            <>
              <svg className="h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              Subscribing...
            </>
          ) : (
            "Subscribe"
          )}
        </button>
      </div>

      {/* How it works — secondary info */}
      <details className="group rounded-lg border border-gray-200 bg-white">
        <summary className="flex cursor-pointer items-center gap-2 px-5 py-3 text-sm font-medium text-gray-600 hover:text-gray-900">
          <svg className="h-4 w-4 text-gray-400 transition-transform group-open:rotate-90" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
          How does this work?
        </summary>
        <div className="border-t border-gray-100 px-5 py-4">
          <ul className="space-y-2 text-xs leading-relaxed text-gray-600">
            <li className="flex items-start gap-2">
              <svg className="mt-0.5 h-3 w-3 shrink-0 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
              We scan council agendas, minutes, and meeting videos from your selected municipalities every 30 minutes.
            </li>
            <li className="flex items-start gap-2">
              <svg className="mt-0.5 h-3 w-3 shrink-0 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" /></svg>
              AI summarizes relevant items matching your topics and keywords.
            </li>
            <li className="flex items-start gap-2">
              <svg className="mt-0.5 h-3 w-3 shrink-0 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
              <strong>Immediate alerts</strong> (if enabled) are sent within minutes of a new match.
            </li>
            <li className="flex items-start gap-2">
              <svg className="mt-0.5 h-3 w-3 shrink-0 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
              <strong>Weekly digest</strong> is sent every Sunday at 8 PM Pacific with a full summary.
            </li>
          </ul>
        </div>
      </details>
    </form>
  );
}
