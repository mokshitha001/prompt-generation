from fastapi import FastAPI
from models import models
from database.db_connect import engine
from api.routes import router

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(router)

