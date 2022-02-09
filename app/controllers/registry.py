### Register templated controllers and the main app router will automatically pick them up

# MUST include properties: router, prefix, and tags
from app.controllers.api import main

WEB_CONTROLLERS = []

API_CONTROLLERS = [main]
