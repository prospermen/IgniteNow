from fastapi import APIRouter

from . import admin, analytics, auth, demo, interactions, player, system, uploads

router = APIRouter(prefix="/api")
router.include_router(admin.router)
router.include_router(auth.router)
router.include_router(uploads.router)
router.include_router(player.router)
router.include_router(interactions.router)
router.include_router(analytics.router)
router.include_router(system.router)
router.include_router(demo.router)
