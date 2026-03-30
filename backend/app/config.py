from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "BC Local Government Council Tracker"
    debug: bool = False
    app_base_url: str = ""  # e.g. https://your-domain.com (no trailing slash)

    # Neon Postgres
    database_url: str = "postgresql+asyncpg://localhost:5432/hearing_watch"
    database_url_sync: str = "postgresql://localhost:5432/hearing_watch"

    # Gemini
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"

    # Perplexity
    perplexity_api_key: str = ""

    # SMTP (Hostinger email)
    smtp_host: str = "smtp.hostinger.com"
    smtp_port: int = 465
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_from_email: str = "BC Local Government Council Tracker <noreply@lg-tracker.ca>"

    # CORS — comma-separated list of allowed origins
    # e.g. "http://localhost:3000,https://yourdomain.com"
    allowed_origins: str = "http://localhost:3000"

    # Cron secret — protects cron and admin endpoints from unauthorized invocation.
    # Set to any non-empty string in production. Callers must send:
    #   X-Cron-Secret: <value>
    cron_secret: str = ""

    # Logging — "json" for structured JSON output, "text" for human-readable
    log_format: str = "text"

    # Scraping
    request_delay_seconds: float = 2.0
    scrape_timeout_seconds: int = 30
    user_agent: str = "BCHearingWatch/0.1 (public-data municipal meeting tracker)"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
