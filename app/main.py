from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import index

app = FastAPI(
    title="BugBuster Labs", description="A playground for web application security."
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(index.router)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
