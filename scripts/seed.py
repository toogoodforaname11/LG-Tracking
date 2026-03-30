#!/usr/bin/env python3
"""Seed the database with BC municipality and source data.

Usage (from the repo root):
    cd backend && python -m scripts.seed_runner

Or using the deploy script which calls this automatically.

Idempotent — safe to run multiple times.  Existing municipalities
(matched by short_name) are skipped; new sources are added.

Requires DATABASE_URL_SYNC in backend/.env (or as an environment variable).
"""

import asyncio
import os
import sys

# Ensure the backend package is importable
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backend")
sys.path.insert(0, backend_dir)

# Change to backend dir so pydantic-settings finds .env
os.chdir(backend_dir)

from app.db.database import async_session  # noqa: E402
from app.services.seed_registry import seed_registry  # noqa: E402


async def main() -> None:
    print("Seeding database with BC municipality data...")
    async with async_session() as session:
        stats = await seed_registry(session)

    print(
        f"Done — {stats['municipalities_created']} municipalities created, "
        f"{stats['municipalities_existed']} already existed, "
        f"{stats['sources_created']} sources created."
    )


if __name__ == "__main__":
    asyncio.run(main())
