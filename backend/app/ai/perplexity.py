"""Perplexity Search API for verification of AI-generated summaries."""

import json
import logging

import httpx

from app.config import settings

logger = logging.getLogger(__name__)

VERIFY_PROMPT = """Verify the following claims about a BC local government hearing/meeting.
For each claim, check if it can be confirmed from publicly available sources.

Municipality: {municipality}
Meeting date: {meeting_date}
Document type: {document_type}

Claims to verify:
{claims}

For each claim, respond with:
- CONFIRMED: if you found corroborating public sources
- UNCONFIRMED: if you couldn't find evidence either way
- INCORRECT: if the claim contradicts available information

Include source URLs where possible.

Respond in JSON:
{{
  "verification_status": "verified" | "partially_verified" | "unverified",
  "claims": [
    {{
      "claim": "...",
      "status": "confirmed" | "unconfirmed" | "incorrect",
      "source_url": "..." or null,
      "note": "..."
    }}
  ],
  "overall_confidence": 0.0-1.0,
  "sources_checked": ["url1", "url2"]
}}"""


async def verify_with_perplexity(
    municipality: str,
    meeting_date: str,
    document_type: str,
    key_points: list[str],
) -> dict | None:
    """Verify key points using Perplexity Search API.

    Returns verification result dict or None if API unavailable.
    """
    if not settings.perplexity_api_key:
        logger.warning("Perplexity API key not set — skipping verification")
        return None

    claims_text = "\n".join(f"- {point}" for point in key_points)
    prompt = VERIFY_PROMPT.format(
        municipality=municipality,
        meeting_date=meeting_date,
        document_type=document_type,
        claims=claims_text,
    )

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.perplexity_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "sonar",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a fact-checker for BC municipal government information. Be precise and cite sources.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.1,
                    "max_tokens": 1500,
                },
            )
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]

            # Try to parse as JSON
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # If not JSON, return as raw text
                return {
                    "verification_status": "unverified",
                    "raw_response": content,
                    "overall_confidence": 0.0,
                }

    except Exception as e:
        logger.error(f"Perplexity verification failed: {e}")
        return None
