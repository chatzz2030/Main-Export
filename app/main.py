"""FastAPI application entry point and route registration."""
from fastapi import FastAPI
from app.routes.synopsis import router as synopsis_router

app = FastAPI(title="Video Synopsis Exporter Engine")

app.include_router(synopsis_router)
