from fastapi import APIRouter

hello_router = APIRouter()


@hello_router.get("/helloworld")
async def helloworld():
    return {"message": "Hello, world!"}
