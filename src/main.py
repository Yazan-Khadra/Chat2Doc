from fastapi import FastAPI
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings

app = FastAPI()


@app.on_event("startup")
async def startup_db_client():
    setting = get_settings()

    app.state.mongo_connection = AsyncIOMotorClient(
        setting.MONGO_DB_URI
    )

    app.state.mongo_db = app.state.mongo_connection[
        setting.MONGO_DB_NAME
    ]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.state.mongo_connection.close()


app.include_router(base.base_router)
app.include_router(data.data_router)