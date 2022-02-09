from fastapi import APIRouter

from app.controllers.registry import WEB_CONTROLLERS

main_router = APIRouter(include_in_schema=False)

for controller in WEB_CONTROLLERS:
    main_router.include_router(
        controller.router, prefix=controller.prefix, tags=controller.tags
    )
