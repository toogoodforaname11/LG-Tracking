"""Gemini AI client for matching and summarization.

Supports batching to reduce API costs — multiple documents can be
matched or summarized in a single Gemini call.
"""

import json
import logging

from app.config import settings

logger = logging.getLogger(__name__)

# Lazy import — only needed when actually calling Gemini
_genai = None
_model = None

# Batch size limits
MATCH_BATCH_SIZE = 10  # Match up to 10 docs per Gemini call
SUMMARY_BATCH_SIZE = 5  # Summarize up to 5 docs per call (summaries are larger)


def _get_model():
    global _genai, _model
    if _model is None:
        import google.generativeai as genai
        genai.configure(api_key=settings.gemini_api_key)
        _genai = genai
        _model = genai.GenerativeModel(settings.gemini_model)
    return _model


async def gemini_match(prompt: str) -> dict | None:
    """Run a matching prompt and parse JSON response."""
    if not settings.gemini_api_key:
        logger.warning("Gemini API key not set — using keyword fallback matching")
        return None

    try:
        model = _get_model()
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.1,
                "max_output_tokens": 500,
                "response_mime_type": "application/json",
            },
        )
        return json.loads(response.text)
    except json.JSONDecodeError:
        logger.error(f"Gemini returned non-JSON response: {response.text[:200]}")
        return None
    except Exception as e:
        logger.error(f"Gemini match call failed: {e}")
        return None


async def gemini_batch_match(prompt: str) -> list[dict] | None:
    """Run a batch matching prompt. Returns list of match results per document."""
    if not settings.gemini_api_key:
        return None

    try:
        model = _get_model()
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.1,
                "max_output_tokens": 2000,
                "response_mime_type": "application/json",
            },
        )
        result = json.loads(response.text)
        # Handle both array and object responses
        if isinstance(result, list):
            return result
        if isinstance(result, dict) and "results" in result:
            return result["results"]
        return [result]
    except json.JSONDecodeError:
        logger.error(f"Gemini batch match returned non-JSON: {response.text[:200]}")
        return None
    except Exception as e:
        logger.error(f"Gemini batch match failed: {e}")
        return None


async def gemini_summarize(prompt: str) -> dict | None:
    """Run a summarization prompt and parse JSON response."""
    if not settings.gemini_api_key:
        logger.warning("Gemini API key not set — skipping summarization")
        return None

    try:
        model = _get_model()
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.3,
                "max_output_tokens": 2000,
                "response_mime_type": "application/json",
            },
        )
        return json.loads(response.text)
    except json.JSONDecodeError:
        logger.error(f"Gemini returned non-JSON for summary: {response.text[:200]}")
        return None
    except Exception as e:
        logger.error(f"Gemini summarize call failed: {e}")
        return None


async def gemini_batch_summarize(prompt: str) -> list[dict] | None:
    """Run a batch summarization prompt. Returns list of summaries per document."""
    if not settings.gemini_api_key:
        return None

    try:
        model = _get_model()
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.3,
                "max_output_tokens": 5000,
                "response_mime_type": "application/json",
            },
        )
        result = json.loads(response.text)
        if isinstance(result, list):
            return result
        if isinstance(result, dict) and "results" in result:
            return result["results"]
        return [result]
    except json.JSONDecodeError:
        logger.error(f"Gemini batch summary returned non-JSON: {response.text[:200]}")
        return None
    except Exception as e:
        logger.error(f"Gemini batch summary failed: {e}")
        return None


async def gemini_embed(text: str) -> list[float] | None:
    """Generate embedding for text using Gemini text-embedding-004."""
    if not settings.gemini_api_key:
        return None

    try:
        if _genai is None:
            _get_model()  # Initialize genai
        result = _genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="retrieval_document",
        )
        return result["embedding"]
    except Exception as e:
        logger.error(f"Gemini embed call failed: {e}")
        return None


async def gemini_batch_embed(texts: list[str]) -> list[list[float] | None]:
    """Batch embed multiple texts in a single API call.

    Gemini embed_content supports batching natively — pass a list of strings.
    This reduces API calls from N to 1.
    """
    if not settings.gemini_api_key:
        return [None] * len(texts)

    try:
        if _genai is None:
            _get_model()

        # Gemini embed_content accepts a list for batch embedding
        result = _genai.embed_content(
            model="models/text-embedding-004",
            content=texts,
            task_type="retrieval_document",
        )
        return result["embedding"]
    except Exception as e:
        logger.error(f"Gemini batch embed failed: {e}")
        # Fallback: try individual embeds
        embeddings = []
        for text in texts:
            embeddings.append(await gemini_embed(text))
        return embeddings


def _is_bylaw_keyword(kw: str) -> bool:
    """Check if a keyword looks like a specific bylaw number, bill, or act name."""
    kw_lower = kw.strip().lower()
    import re
    # Matches patterns like "bylaw 1700", "bl 1700", "bill 44", or act names
    return bool(re.match(r"^(bylaw|by-law|bl|bill)\s+\d+", kw_lower)) or "act" in kw_lower


def keyword_fallback_match(
    content: str, topics: list[str], keywords: list[str]
) -> dict:
    """Simple keyword-based matching when Gemini is unavailable.

    Used as fallback when API key is not set or calls fail.
    Includes exact-match bylaw/bill tracking: if a keyword looks like a bylaw
    number or act name and appears anywhere in the content, it's a high-confidence match.
    """
    content_lower = content.lower()

    # Check for exact bylaw/bill/act keyword matches first (high confidence)
    bylaw_matches = []
    regular_matches = []
    for kw in keywords:
        if kw.lower() in content_lower:
            if _is_bylaw_keyword(kw):
                bylaw_matches.append(kw)
            else:
                regular_matches.append(kw)

    matched_keywords = bylaw_matches + regular_matches

    # Topic keyword mappings — focused on housing/transit/bylaw topics
    topic_keywords = {
        "toa": [
            "transit oriented", "transit-oriented", "toa", "transit area",
            "density near transit", "transit village", "rapid transit",
        ],
        "ssmuh": [
            "small-scale multi-unit", "ssmuh", "duplex", "triplex", "fourplex",
            "four-plex", "missing middle", "multi-unit housing", "small scale multi",
        ],
        "housing_statutes": [
            "housing statutes amendment", "bill 44", "bill 46", "bill 47",
            "housing legislation", "provincial housing", "housing act",
        ],
        "ocp_housing": [
            "official community plan", "ocp", "community plan amendment",
            "ocp amendment", "ocp housing", "housing designation",
        ],
        "zoning_density": [
            "rezone", "rezoning", "zoning amendment", "zoning bylaw",
            "upzoning", "density bonus", "housing density", "zoning for housing",
        ],
        "dev_permits_housing": [
            "development permit", "dp application", "development variance",
            "housing permit", "residential permit", "building permit",
        ],
        "other_housing": [
            "housing", "affordable housing", "rental", "housing strategy",
            "housing bylaw", "housing policy", "residential", "shelter",
            "supportive housing", "social housing", "housing agreement",
        ],
    }

    matched_topics = []
    for topic in topics:
        if topic in topic_keywords:
            if any(tk in content_lower for tk in topic_keywords[topic]):
                matched_topics.append(topic)

    is_match = bool(matched_keywords or matched_topics)

    # Bylaw exact matches get high confidence
    if bylaw_matches:
        confidence = 1.0
    else:
        total_possible = len(keywords) + len(topics)
        total_matched = len(matched_keywords) + len(matched_topics)
        confidence = total_matched / max(total_possible, 1)

    return {
        "is_match": is_match,
        "confidence": min(confidence, 1.0),
        "matched_topics": matched_topics,
        "matched_keywords": matched_keywords,
        "reason": (
            f"Bylaw exact match: {bylaw_matches}, Keyword match: {regular_matches}, Topic match: {matched_topics}"
            if bylaw_matches
            else f"Keyword match: {matched_keywords}, Topic match: {matched_topics}"
            if is_match
            else "No keyword or topic matches found"
        ),
    }
