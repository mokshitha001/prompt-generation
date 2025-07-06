from fastapi import FastAPI
from models.orm_models import Base
from database.db import engine
from api.routes import router
from api.prompt.prompt_routes import router as prompt_router
Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(router)
app.include_router(prompt_router)
