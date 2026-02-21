from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.database.database import connect_to_mongo, close_mongo_connection
from fastapi.middleware.cors import CORSMiddleware

from core.apis.routers.user_router import user_router
from core.apis.routers.order_router import order_router
from core import logger

logging = logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logging.info("Starting User Management API")
        await connect_to_mongo()
    except Exception as e:
        logging.error(f"Error connecting to MongoDB: {e}")
    yield
    logging.info("Shutting down User Management API")
    await close_mongo_connection()


app = FastAPI(
    title="User Management API",
    description="API for user management",
    version="1.0.0",
    lifespan=lifespan,
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, tags=["User Management"])
app.include_router(order_router, tags=["Order Management"])


@app.get("/", tags=["Health"])
async def root():
    return {"message": "Welcome to the User Management API!"}
