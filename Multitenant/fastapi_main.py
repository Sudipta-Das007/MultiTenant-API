from db import models
from db.database import engine
from fastapi import FastAPI
from router import add_api, delete_api, update_api, login_api, view_api, search_api
from auth import authentication

pattern = "^[a-zA-Z\s-]*$"


# creating database tables
models.Base.metadata.create_all(engine)


app = FastAPI()


app.include_router(add_api.router)

app.include_router(delete_api.router)

app.include_router(update_api.router)

app.include_router(login_api.router)

app.include_router(search_api.router)

app.include_router(view_api.router)

app.include_router(authentication.router)


