from fastapi import FastAPI

from db.session import engine
from db.models import Base
from api.r_services.services import router as services_router


app = FastAPI()


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(services_router, tags=['services'], prefix='/services')