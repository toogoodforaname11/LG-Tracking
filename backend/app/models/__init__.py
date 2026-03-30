# Import all models so SQLAlchemy metadata picks them up
from app.models.municipality import Municipality, Source, ScrapeRun  # noqa: F401
from app.models.document import Meeting, Document  # noqa: F401
from app.models.track import Track, TrackMatch  # noqa: F401
from app.models.subscriber import Subscriber  # noqa: F401
from app.models.api_cost_log import ApiCostLog  # noqa: F401
from app.models.magic_link import MagicLinkToken  # noqa: F401
