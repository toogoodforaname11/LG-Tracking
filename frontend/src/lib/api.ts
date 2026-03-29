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

// --- Subscribe ---

export interface SubscribeRequest {
  email: string;
  municipalities: string[];
  topics: string[];
  keywords: string;
  immediate_alerts: boolean;
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
  website_url: string | null;
  population: number | null;
  is_active: boolean;
  sources: Source[];
}

export interface MunicipalityListResponse {
  municipalities: Municipality[];
  total: number;
}

export async function getMunicipalities(): Promise<MunicipalityListResponse> {
  return apiFetch("/api/v1/municipalities");
}
