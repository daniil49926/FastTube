from fastapi import APIRouter

healthchecker_router_v1 = APIRouter()


@healthchecker_router_v1.get("/test")
def test():
    return {"result": "OK"}
