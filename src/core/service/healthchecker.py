from fastapi import APIRouter

healthchecker_router_v1 = APIRouter()


@healthchecker_router_v1.get("/test")
def healthchecker_test():
    return {"result": "OK"}
