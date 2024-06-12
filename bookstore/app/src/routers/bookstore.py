import asyncio
from typing import List, Dict, Optional, Union
from fastapi import Depends, status, HTTPException, Request
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from logging import getLogger
from app.src.utils.router import APIRouter
from app.src.schemas.bookstore_request import BookCreate as StoreRequestSchema, BookUpdate
from app.src.schemas.bookstore_response import RegistryResponse as ResponseSchema, UpdateResponse
from app.src.schemas.bookstore_response import BookStore, CategoryBooks, Book
from app.src.database import get_db
from app.src.constants import StoreConstants as Sc
import app.src.cruds.bookstore as crud

router = APIRouter()
logger = getLogger(__name__)


# Custom dependency to validate query parameters
def validate_query_params(request: Request):
    ALLOWED_QUERY_PARAMS = {"query", "category"}
    query_params = request.query_params
    for param in query_params:
        if param not in ALLOWED_QUERY_PARAMS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid query parameter: {param}"
            )


@router.get('/',
            status_code=status.HTTP_200_OK,
            response_model=Union[List[CategoryBooks], List[BookStore]],
            dependencies=[Depends(validate_query_params)],
            summary="Get Store information",
            description="Get Store information")
def get_books(query: Optional[str] = None,
              category: Optional[str] = None):
    """
        GET response method for all the books.
        :return: Json response
    """
    db = next(get_db())
    try:
        if query:
            result = crud.fetch_book_details_with_partial_keyword_match(store_db=db, query=query)
        elif category:
            result = crud.fetch_books_with_category(store_db=db, category=category)
        else:
            books = crud.fetch_books(store_db=db)
            grouped_books: Dict[str, List[Book]] = {}
            for book in books:
                if book.category not in grouped_books:
                    grouped_books[book.category] = []
                grouped_books[book.category].append(Book.from_orm(book))

            result = [
                CategoryBooks(category=category, books=books)
                for category, books in grouped_books.items()
            ]

        logger.debug("Response Returned: %s", str(result))
        return result

    except asyncio.CancelledError as exe:
        logger.error(f"asyncio cancellation error {exe}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=Sc.RESPONSE_MSG_500)


@router.post('/', status_code=status.HTTP_201_CREATED,
             response_model=ResponseSchema, summary="Create a resource",
             description="Create a resource for store having details about the store")
def create_store_resource(store_obj: StoreRequestSchema, db_obj=Depends(get_db)):
    try:
        result = crud.create_book_store(db_obj, store_obj)
        return result
    except asyncio.CancelledError as exe:
        logger.error(f"asyncio cancellation error {exe}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=Sc.RESPONSE_MSG_500)


@router.put("/{book_id}",
            status_code=status.HTTP_200_OK,
            response_model=UpdateResponse,
            summary="Updated a resource",
            description="Create a resource for store having details about the store")
def update_book(book_id: int, book: BookUpdate):
    db_obj = next(get_db())
    try:
        result = crud.update_book_store(db_obj, book_id, book)
        return result
    except asyncio.CancelledError as exe:
        logger.error(f"asyncio cancellation error {exe}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=Sc.RESPONSE_MSG_500)
