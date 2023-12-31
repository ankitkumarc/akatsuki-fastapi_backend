from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.retailer_model import User
from app.models.customer_model import Customer
from app.models.coupon_model import Coupon
from app.core.config import settings
from app.api.api_v1.router import router 
from app.models.purchase_model import Purchase


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


@app.on_event("startup")
async def app_init():
    """
    Initialize crucial application services
    """
    
    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING).retailsense

    await init_beanie(
        database=db_client,
        document_models=[
            User,
            Customer,
            Coupon,
            Purchase
        ]
    )


app.include_router(router, prefix=settings.API_V1_STR)