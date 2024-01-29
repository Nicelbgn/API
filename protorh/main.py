from fastapi import FastAPI
from routes.user_route import route_user
from routes.rh_route import route_rh
from fastapi import FastAPI

app = FastAPI()

app.include_router(route_user)
app.include_router(route_rh)


@app.get("/")
async def read_root():
    return {"message": "Hello World!"}


