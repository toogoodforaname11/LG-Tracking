from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "BC Hearing Watch"
    debug: bool = True

    # Neon Postgres
    database_url: str = "postgresql+asyncpg://localhost:5432/hearing_watch"
    database_url_sync: str = "postgresql://localhost:5432/hearing_watch"

    # Gemini
    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-flash"

    # Pinecone
    pinecone_api_key: str = ""
    pinecone_index: str = "hearing-watch"

    # Perplexity
    perplexity_api_key: str = ""

    # Resend (email)
    resend_api_key: str = ""
    resend_from_email: str = "BC Hearing Watch <noreply@bchearingwatch.ca>"

    # Scraping
    request_delay_seconds: float = 2.0
    scrape_timeout_seconds: int = 30
    user_agent: str = "BCHearingWatch/0.1 (public-data municipal meeting tracker)"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
