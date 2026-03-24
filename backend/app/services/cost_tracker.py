"""Cost tracker — persists per-call token usage and estimated USD costs for AI APIs."""

import logging
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.api_cost_log import ApiCostLog

logger = logging.getLogger(__name__)

# USD cost per token for each service/model
_PRICING: dict[str, dict[str, dict[str, float]]] = {
    "gemini": {
        "gemini-1.5-flash": {
            "input": 0.075 / 1_000_000,   # $0.075 per 1M input tokens
            "output": 0.300 / 1_000_000,   # $0.30  per 1M output tokens
        },
    },
    "perplexity": {
        "sonar": {
            "input": 1.00 / 1_000_000,    # $1.00 per 1M input tokens
            "output": 1.00 / 1_000_000,   # $1.00 per 1M output tokens
        },
    },
}


def estimate_cost(service: str, model: str, input_tokens: int, output_tokens: int) -> float:
    """Return estimated USD cost for a single API call."""
    rates = _PRICING.get(service, {}).get(model)
    if not rates:
        return 0.0
    return input_tokens * rates["input"] + output_tokens * rates["output"]


async def log_api_cost(
    db: AsyncSession,
    service: str,
    operation: str,
    model: str,
    input_tokens: int,
    output_tokens: int,
    context: dict[str, Any] | None = None,
) -> None:
    """Write one ApiCostLog row. Silently swallows errors so cost logging never breaks the pipeline."""
    try:
        cost = estimate_cost(service, model, input_tokens, output_tokens)
        record = ApiCostLog(
            service=service,
            operation=operation,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            estimated_cost_usd=cost,
            call_context=context,
        )
        db.add(record)
        await db.flush()
        logger.debug(
            f"Cost logged: {service}/{operation} — "
            f"{input_tokens}in + {output_tokens}out = ${cost:.6f}"
        )
    except Exception as exc:
        logger.warning(f"Failed to log API cost (non-fatal): {exc}")
