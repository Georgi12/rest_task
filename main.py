import uvicorn as uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from api.views import rest_router
from errors.errors import ServiceException
from loguru import logger

app = FastAPI()


app.include_router(rest_router)


@app.exception_handler(ServiceException)
async def exception_handler(request: Request, exc: ServiceException):
    logger.error(f"request: {request.url} error status: {exc.status}, error description: {exc.description}")
    return JSONResponse(
        status_code=exc.status,
        content={"message": exc.description},
    )


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    logger.error(f"request: {request.url} error status: 500, error description: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": str(exc)},
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host='localhost',
        port=8000,
    )
