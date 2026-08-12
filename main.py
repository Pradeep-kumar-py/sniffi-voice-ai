from core.database import init_db
from starlette.responses import FileResponse
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from voice.router import router as voice_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Sniffi Voice AI", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return FileResponse("static/index.html")


app.include_router(voice_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=5000, reload=True)