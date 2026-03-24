"""Gemini AI client for matching and summarization."""

import json
import logging
from typing import Any

from app.config import settings

logger = logging.getLogger(__name__)

# Lazy import — only needed when actually calling Gemini
_genai = None
_model = None


def _get_model():
    global _genai, _model
    if _model is None:
        import google.generativeai as genai
        genai.configure(api_key=settings.gemini_api_key)
        _genai = genai
        _model = genai.GenerativeModel(settings.gemini_model)
    return _model


async def gemini_match(prompt: str) -> dict:
    """Run a matching prompt and parse JSON response.

    Returns parsed dict or a fallback if parsing fails.
    """
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


async def gemini_summarize(prompt: str) -> dict:
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


async def gemini_embed(text: str) -> list[float] | None:
    """Generate embedding for text using Gemini Embedding-2."""
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


def keyword_fallback_match(
    content: str, topics: list[str], keywords: list[str]
) -> dict:
    """Simple keyword-based matching when Gemini is unavailable.

    Used as fallback when API key is not set or calls fail.
    """
    content_lower = content.lower()
    matched_keywords = [kw for kw in keywords if kw.lower() in content_lower]

    # Topic keyword mappings
    topic_keywords = {
        "ocp_updates": ["official community plan", "ocp", "community plan amendment"],
        "rezoning": ["rezone", "rezoning", "zoning amendment", "zoning bylaw"],
        "development_permits": ["development permit", "dp application", "development variance"],
        "public_hearings": ["public hearing", "statutory hearing"],
        "bylaws": ["bylaw", "by-law", "bylaw amendment"],
        "budget": ["budget", "financial plan", "tax rate", "revenue"],
        "environment": ["environment", "climate", "watershed", "stormwater", "emissions"],
        "transportation": ["transportation", "transit", "cycling", "road", "traffic"],
        "housing": ["housing", "affordable housing", "rental", "housing strategy"],
        "parks_recreation": ["park", "recreation", "trail", "community centre"],
        "utilities": ["water", "sewer", "utility", "infrastructure"],
        "governance": ["governance", "council procedure", "election", "boundary"],
    }

    matched_topics = []
    for topic in topics:
        if topic in topic_keywords:
            if any(tk in content_lower for tk in topic_keywords[topic]):
                matched_topics.append(topic)

    is_match = bool(matched_keywords or matched_topics)
    total_possible = len(keywords) + len(topics)
    total_matched = len(matched_keywords) + len(matched_topics)
    confidence = total_matched / max(total_possible, 1)

    return {
        "is_match": is_match,
        "confidence": min(confidence, 1.0),
        "matched_topics": matched_topics,
        "matched_keywords": matched_keywords,
        "reason": (
            f"Keyword match: {matched_keywords}, Topic match: {matched_topics}"
            if is_match
            else "No keyword or topic matches found"
        ),
    }
