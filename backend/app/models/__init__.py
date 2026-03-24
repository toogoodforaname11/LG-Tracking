# Import all models so SQLAlchemy metadata picks them up
from app.models.municipality import Municipality, Source, ScrapeRun  # noqa: F401
from app.models.document import Meeting, Document  # noqa: F401
from app.models.track import Track, TrackMatch  # noqa: F401
