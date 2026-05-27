from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import FileResponse

from .core.logger import setup_logger
from .database import Base, engine
from .middleware.logging_middleware import LoggingMiddleware
from .routers.api import router

Base.metadata.create_all(bind=engine)


class SpaStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        try:
            return await super().get_response(path, scope)
        except StarletteHTTPException as exc:
            if exc.status_code == 404 and "." not in Path(path).name:
                return FileResponse(Path(self.directory) / "index.html")
            raise

setup_logger()

app = FastAPI(title="IgniteNow API", version="0.1.0")
app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "IgniteNow API"}


admin_dist = Path(__file__).resolve().parents[2] / "frontend" / "admin_web" / "dist"
if admin_dist.exists():
    app.mount("/", SpaStaticFiles(directory=admin_dist, html=True), name="admin_web")
