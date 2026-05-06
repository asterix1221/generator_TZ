from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import traceback

from app.db.database import init_db
from app.api import auth, specifications, export, public
from app.core.exceptions import AppException

logger = logging.getLogger("generator_tz")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Generator TZ API")
    try:
        await init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.warning(f"Database init skipped (expected in tests): {e}")
    yield
    logger.info("Shutting down Generator TZ API")


app = FastAPI(
    title="Generator TZ API",
    description="API для генератора технических заданий",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Global exception handler
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}\n{traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Внутренняя ошибка сервера"},
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
