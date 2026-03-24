const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

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

// --- Registry (kept for seed endpoint) ---

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

export async function getMunicipalities(): Promise<{
  municipalities: Municipality[];
  total: number;
}> {
  return apiFetch("/api/v1/municipalities");
}

export async function seedRegistry(): Promise<{
  municipalities_created: number;
  municipalities_existed: number;
  sources_created: number;
}> {
  return apiFetch("/api/v1/seed", { method: "POST" });
}

// --- Discovery (kept for backend cron) ---

export async function triggerPoll(municipality?: string): Promise<unknown> {
  const params = municipality ? `?municipality=${municipality}` : "";
  return apiFetch(`/api/v1/discovery/poll${params}`, { method: "POST" });
}

// --- Processing (kept for backend cron) ---

export async function triggerProcessing(): Promise<unknown> {
  return apiFetch("/api/v1/ai/process", { method: "POST" });
}
