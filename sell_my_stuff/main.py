from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sell_my_stuff.api.api import router

app = FastAPI(title="Sell My Stuff", description="Analyze items and generate sales listings")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Sell My Stuff API - Use /listings/analyze to analyze images"}

app.include_router(router)
