#!/usr/bin/env python

# FastAPI Imports
from fastapi import FastAPI

# Internal
from app.routes import api_router, web_router
from app.config import Config

config = Config()

# Main App
app = FastAPI(
    title=config.app.PROJECT_NAME,
    description=config.app.PROJECT_DESCRIPTION,
    version=config.app.VERSION,
)


# App Events
@app.on_event("startup")
async def setup():
    app.state.config = config


@app.on_event("shutdown")
async def teardown():
    pass


# Apply dynamic routers
app.include_router(api_router)
app.include_router(web_router)
