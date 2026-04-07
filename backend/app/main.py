from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db.database import init_db
from app.api import auth, specifications, export, public


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="Generator TZ API",
    description="API для генератора технических заданий",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(specifications.router)
app.include_router(export.router)
app.include_router(public.router)


@app.get("/")
async def root():
    return {"message": "Generator TZ API", "docs": "/docs"}


@app.get("/health")
async def health():
    return {"status": "healthy"}