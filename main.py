from core.database import init_db
from core.database import engine
from core.database import Base
from starlette.responses import FileResponse
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Sniffi Voice AI", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return FileResponse("static/index.html")



if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=5000, reload=True)