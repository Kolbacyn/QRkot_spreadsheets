from fastapi import APIRouter

from app.api.endpoints.donation import router as donation_router
from app.api.endpoints.google_api import router as google_api_router
from app.api.endpoints.project import router as project_router
from app.api.endpoints.user import router as user_router

main_router = APIRouter()
main_router.include_router(
    donation_router,
    prefix='/donation',
    tags=['Donations']
)
main_router.include_router(
    project_router,
    prefix='/charity_project',
    tags=['Charity projects']
)
main_router.include_router(
    user_router
)
main_router.include_router(
    google_api_router,
    prefix='/google',
    tags=['Google']
)
