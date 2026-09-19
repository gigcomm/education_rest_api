import logging
from collections.abc import Callable
from itertools import count
from time import perf_counter

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import load_settings
from app.core.logging import configure_logging
from app.routers.category import category_router
from app.routers.tasks import task_router

# @asynccontextmanager
# async def lifespan(_: FastAPI):
#     Base.metadata.create_all(bind=engine)
#     yield

configure_logging()
config = load_settings()
app = FastAPI()

logger = logging.getLogger("app.middleware")

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_origins,
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"],
)

request_numbers = count(start=1)


@app.middleware(
    "http"
)  # log_requests выполнится до и после обработки каждого HTTP-запроса
async def log_requests(request: Request, call_next: Callable) -> Response:
    started_at = perf_counter()
    try:
        response: Response = await call_next(request)  # Работа самого эндпоинта
    except Exception:
        duration_ms = (perf_counter() - started_at) * 1000
        logger.exception(
            "Request failed: %s %s completed_in=%.2fms",
            request.method,
            request.url.path,
            duration_ms,
        )
        raise

    duration_ms = (perf_counter() - started_at) * 1000
    logger.info(
        "%s %s -> %s (%.2f ms)",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    response.headers["X-Request-Number"] = str(request_numbers)
    return response


app.include_router(router=task_router)
app.include_router(router=category_router)
