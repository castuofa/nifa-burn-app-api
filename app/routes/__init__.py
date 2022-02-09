from .api import main_router as api_router
from .web import main_router as web_router


__all__ = ["api_router", "web_router"]
