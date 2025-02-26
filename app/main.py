from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import index, xss, api

app = FastAPI(
    title="BugBuster Labs",
    description="A playground for web application security.",
    docs_url="/api/docs",
    redoc_url=None,
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(index.router)
app.include_router(xss.router)
app.include_router(api.router)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
