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

// --- Tracks ---

export interface Track {
  id: number;
  user_id: string;
  name: string;
  municipality_ids: number[];
  topics: string[];
  keywords: string[];
  is_active: boolean;
  notify_email: boolean;
  created_at: string;
  updated_at: string;
}

export interface TrackMatch {
  id: number;
  track_id: number;
  document_id: number;
  match_score: number | null;
  match_reason: string | null;
  matched_topics: string[] | null;
  matched_keywords: string[] | null;
  summary: string | null;
  verification_status: string | null;
  notified_at: string | null;
}

export async function getTracks(): Promise<Track[]> {
  return apiFetch("/api/v1/tracks");
}

export async function createTrack(data: {
  name: string;
  municipality_ids: number[];
  topics: string[];
  keywords: string[];
}): Promise<Track> {
  return apiFetch("/api/v1/tracks", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function deleteTrack(id: number): Promise<void> {
  return apiFetch(`/api/v1/tracks/${id}`, { method: "DELETE" });
}

export async function getTrackMatches(trackId: number): Promise<TrackMatch[]> {
  return apiFetch(`/api/v1/tracks/${trackId}/matches`);
}

export async function getTopics(): Promise<{ topics: string[] }> {
  return apiFetch("/api/v1/topics");
}

// --- Discovery ---

export async function triggerPoll(municipality?: string): Promise<unknown> {
  const params = municipality ? `?municipality=${municipality}` : "";
  return apiFetch(`/api/v1/discovery/poll${params}`, { method: "POST" });
}

export async function getDocuments(newOnly = false): Promise<unknown[]> {
  return apiFetch(`/api/v1/discovery/documents?new_only=${newOnly}`);
}

// --- Processing ---

export async function triggerProcessing(): Promise<unknown> {
  return apiFetch("/api/v1/ai/process", { method: "POST" });
}

// --- Alerts ---

export async function triggerNotify(): Promise<unknown> {
  return apiFetch("/api/v1/alerts/notify", { method: "POST" });
}

export async function getDigest(trackId: number): Promise<unknown> {
  return apiFetch(`/api/v1/alerts/digest/${trackId}`);
}
