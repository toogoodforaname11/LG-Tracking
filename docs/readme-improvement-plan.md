# README Improvement Plan

This plan outlines phased improvements for keeping the repository documentation accurate, practical, and project-focused.

## Phase 1: Clean Up README Positioning

Goal: make the README read like a direct project README for a civic technology application.

- Remove recruiter, portfolio, hiring, and resume-oriented language.
- Present the application as a local government tracking tool.
- Keep project status honest: work-in-progress prototype unless production status is verified.
- Replace reviewer-oriented roadmap language with neutral future-development language.
- Keep setup, usage, architecture, and deployment sections focused on users and contributors.

## Phase 2: Verify Technical Accuracy

Goal: ensure every README claim is supported by the repository.

- Confirm setup commands work from a clean clone.
- Verify backend dependency installation instructions.
- Verify database migration and seed commands.
- Confirm frontend development and build commands.
- Check whether backend tests currently pass.
- Remove or qualify any unverified deployment, coverage, or production claims.

## Phase 3: Improve Operational Documentation

Goal: make the project easier to run and maintain.

- Add a clearer local development flow.
- Add a minimum viable setup path for users who do not want email or AI integrations.
- Clarify which environment variables are required locally versus in production.
- Document cron and admin endpoint usage with the `X-Cron-Secret` header.
- Add troubleshooting notes for common startup issues.

## Phase 4: Add Project Evidence

Goal: show what the application does without overstating its status.

- Add screenshots of the subscription form.
- Add an anonymized example alert email or digest.
- Add an architecture diagram showing:
  - Next.js frontend
  - FastAPI backend
  - PostgreSQL database
  - Scrapers
  - Scheduled jobs
  - Email delivery
  - Optional AI services

## Phase 5: Repository Hygiene

Goal: make the repository cleaner and easier to maintain.

- Add a license file if public reuse is intended.
- Add CI checks for backend tests, frontend builds, and linting if supported.
- Fix or remove unsupported package scripts.
- Add sample development data or fixtures for easier local evaluation.
- Consider moving long deployment details into `docs/deployment.md` if the README becomes too long.

## Phase 6: Testing and Reliability Improvements

Goal: make the application safer to change.

- Document current backend test coverage.
- Add frontend tests for the subscription form.
- Add tests for environment and configuration validation.
- Document scraper failure handling.
- Document source health and status handling.
- Add observability notes for polling, email delivery, and AI-processing failures.

## Phase 7: Deployment Clarity

Goal: avoid implying deployment status that has not been verified.

- State whether the application is currently deployed only if there is a verified URL.
- Clarify supported deployment modes:
  - local development
  - VPS with Nginx, systemd, and cron
  - static frontend export
  - scheduled cron endpoints
- Document required production settings separately from local development settings.
