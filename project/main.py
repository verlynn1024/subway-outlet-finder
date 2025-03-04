import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

from app.api.routes import router as api_router
from app.web.routes import router as web_router
from app.scraper.subway_scraper import SubwayScraper
from app.database.db import init_db

app = FastAPI(title="Subway Outlet Finder")

# Mount static files
app.mount("/static", StaticFiles(directory="app/web/static"), name="static")

# Include routers
app.include_router(api_router, prefix="/api")
app.include_router(web_router)

@app.on_event("startup")
async def startup_event():
    # Initialize database
    init_db()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)