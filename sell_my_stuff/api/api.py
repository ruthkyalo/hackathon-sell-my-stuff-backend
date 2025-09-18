from fastapi import APIRouter

from sell_my_stuff.api.endpoints import listings

router = APIRouter()
router.include_router(listings.router, prefix="/listings", tags=["Listings"])
