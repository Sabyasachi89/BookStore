from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette import status
from starlette.exceptions import HTTPException
from logging import getLogger
from app.src.routers.bookstore import router as store_router
from app.src.utils.router import APIRouter
from app.src.constants import StoreConstants as Sc
from app.src.env import BASE_URL
import uvicorn

logger = getLogger(__name__)

prefix_link = f'{BASE_URL}'

router = APIRouter()
router.include_router(store_router,
                      prefix=prefix_link,
                      tags=['Book Store API Method']
                      )

app = FastAPI(title="Book Store API")
app.include_router(router)


@app.exception_handler(HTTPException)
async def http_exception_handler(requests, exc):
    """
    @param requests:
    @param exc: exception raised from other functions
    @return: json formatted error message along with code
    """
    logger.error("Requests: %s, exc: %s}", requests, exc)
    headers = {"charset": 'UTF-8'}
    return JSONResponse(status_code=exc.status_code,
                        content=jsonable_encoder(
                            {"detail": {"error": {"message":  str(exc.detail)}}}),
                        headers=headers
                        )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(requests, exc):
    """
    @return:json formatted error message along with code
    """
    logger.error("Requests: %s, exc: %s}", requests, exc)
    headers = {"charset": 'UTF-8'}
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        content=jsonable_encoder(
                            {"detail": {"error": {"message": Sc.RESPONSE_MSG_422}}}),
                        headers=headers
                        )
