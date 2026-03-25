"""Cost reporting API — weekly breakdown of AI API token usage and estimated spend."""

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.db.database import get_db
from app.models.api_cost_log import ApiCostLog

router = APIRouter()


@router.get("/costs/weekly")
async def get_weekly_costs(
    weeks_back: int = Query(default=1, ge=1, le=52, description="How many weeks back to report"),
    db: AsyncSession = Depends(get_db),
):
    """Return token usage and estimated USD costs grouped by service and operation.

    Covers the last `weeks_back` complete weeks (Mon–Sun), defaulting to the current week.
    """
    now = datetime.now(timezone.utc)
    period_end = now
    period_start = now - timedelta(weeks=weeks_back)

    result = await db.execute(
        select(ApiCostLog).where(
            ApiCostLog.created_at >= period_start,
            ApiCostLog.created_at < period_end,
        )
    )
    logs = result.scalars().all()

    # Aggregate
    by_service: dict = {}
    total_cost = 0.0

    for log in logs:
        svc = by_service.setdefault(log.service, {
            "total_cost_usd": 0.0,
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "call_count": 0,
            "by_operation": {},
        })
        svc["total_cost_usd"] += log.estimated_cost_usd
        svc["total_input_tokens"] += log.input_tokens
        svc["total_output_tokens"] += log.output_tokens
        svc["call_count"] += 1
        total_cost += log.estimated_cost_usd

        op = svc["by_operation"].setdefault(log.operation, {
            "calls": 0,
            "input_tokens": 0,
            "output_tokens": 0,
            "cost_usd": 0.0,
        })
        op["calls"] += 1
        op["input_tokens"] += log.input_tokens
        op["output_tokens"] += log.output_tokens
        op["cost_usd"] += log.estimated_cost_usd

    # Round floats for readability
    total_cost = round(total_cost, 6)
    for svc in by_service.values():
        svc["total_cost_usd"] = round(svc["total_cost_usd"], 6)
        for op in svc["by_operation"].values():
            op["cost_usd"] = round(op["cost_usd"], 6)

    return {
        "period_start": period_start.isoformat(),
        "period_end": period_end.isoformat(),
        "weeks_back": weeks_back,
        "total_calls": len(logs),
        "total_cost_usd": total_cost,
        "by_service": by_service,
    }
