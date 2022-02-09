from fastapi import APIRouter

from app.controllers.registry import API_CONTROLLERS

main_router = APIRouter()

for controller in API_CONTROLLERS:
    main_router.include_router(
        controller.router, prefix=controller.prefix, tags=controller.tags
    )
