from fastapi import FastAPI

from src import root

app = FastAPI()
app.include_router(router=root, prefix="/api")

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
