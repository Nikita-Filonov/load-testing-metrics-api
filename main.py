from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from apps.analytics.api import analytics_app_router
from apps.results.api import results_app_router
from apps.services.api import services_app_router

app = FastAPI(title="Load testing metrics API")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(results_app_router, prefix="/api/v1")
app.include_router(services_app_router, prefix="/api/v1")
app.include_router(analytics_app_router, prefix="/api/v1")
