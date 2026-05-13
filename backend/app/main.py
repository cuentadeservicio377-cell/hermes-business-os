"""
Hermes Business OS - FastAPI Application
Main entry point with routers and middleware
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from core.config import settings, client_config
from core.database import init_db
from app.routers import health, company, clients, projects, documents, skills


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    init_db()
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} starting...")
    print(f"   Company: {client_config.company.get('name', 'Not configured')}")
    print(f"   Departments: {[d.get('name') for d in client_config.departments if d.get('enabled')]}")
    yield
    # Shutdown
    print("👋 Shutting down...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Open source AI operating system for small and medium businesses",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(company.router, prefix="/api/v1", tags=["company"])
app.include_router(clients.router, prefix="/api/v1", tags=["clients"])
app.include_router(projects.router, prefix="/api/v1", tags=["projects"])
app.include_router(documents.router, prefix="/api/v1", tags=["documents"])
app.include_router(skills.router, prefix="/api/v1", tags=["skills"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs"
    }
