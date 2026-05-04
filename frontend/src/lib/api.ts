const API_BASE = process.env.NEXT_PUBLIC_API_URL || "";

async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...options?.headers },
    ...options,
  });
  if (!res.ok) {
    const error = await res.text();
    throw new Error(`API error ${res.status}: ${error}`);
  }
  return res.json();
}

// --- Province ---

// Mirrors the backend's PROVINCE_BC / PROVINCE_AB / PROVINCE_ON constants
// exactly.
export type Province = "BC" | "Alberta" | "Ontario";

// Mirrors the backend's TIER_UPPER / TIER_LOWER / TIER_SINGLE constants.
// Optional on Municipality because older API responses may omit it.
export type Tier = "upper" | "lower" | "single";

// --- Subscribe ---

export interface SubscribeRequest {
  email: string;
  municipalities: string[];
  topics: string[];
  keywords: string;
  immediate_alerts: boolean;
  // Optional for backward compatibility with older callers; the backend
  // defaults to "BC" when omitted.
  province?: Province;
}

export interface SubscribeResponse {
  status: string;
  email: string;
  message: string;
}

export async function subscribe(
  data: SubscribeRequest
): Promise<SubscribeResponse> {
  return apiFetch("/api/v1/subscribe", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

// --- Registry ---

export interface Source {
  id: number;
  platform: string;
  source_type: string;
  url: string;
  label: string;
  scrape_status: string;
  last_scraped_at: string | null;
}

export interface Municipality {
  id: number;
  name: string;
  short_name: string;
  gov_type: string;
  region: string;
  province: string;
  /**
   * Ontario-flavoured tier ("upper", "lower", "single"). Defaults to
   * "single" for BC/AB rows on the backend; optional here to keep the
   * type tolerant of older deployments.
   */
  tier?: Tier;
  website_url: string | null;
  population: number | null;
  is_active: boolean;
  sources: Source[];
}

export interface MunicipalityListResponse {
  municipalities: Municipality[];
  total: number;
}

/**
 * Fetch the registered municipalities, optionally scoped to one province.
 * Pass ``"all"`` to bypass the default-BC filter and return every province
 * in one call (used by admin tooling).
 */
export async function getMunicipalities(
  province?: Province | "all"
): Promise<MunicipalityListResponse> {
  const qs = province ? `?province=${encodeURIComponent(province)}` : "";
  return apiFetch(`/api/v1/municipalities${qs}`);
}
