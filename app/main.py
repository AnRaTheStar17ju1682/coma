from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import uvicorn

from routes import api, files, frontend

from lifespan import lifespan


app = FastAPI(title="Coma-api", lifespan=lifespan)

app.include_router(api.router)
app.include_router(files.router)
app.include_router(frontend.router)
app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    # http://coma.localhost:8000/
    uvicorn.run(app, host="0.0.0.0", port=8000)