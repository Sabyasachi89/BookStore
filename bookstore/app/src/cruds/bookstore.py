from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_409_CONFLICT, HTTP_404_NOT_FOUND
from logging import getLogger
from app.src.models import BookStore
from app.src.schemas.bookstore_request import BookCreate as BookCreateRequestSchema
from app.src.constants import StoreConstants as Sc

logger = getLogger(__name__)


def fetch_books(store_db: Session):
    """
    Fetch book store object containing all book details.
    @param store_db: book store database instance
    @return: book store record objects
    """
    try:
        data = store_db.query(BookStore).all()
        return data
    except Exception as exception:
        logger.error(exception)
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=Sc.RESPONSE_MSG_500) from exception


def fetch_book_details_with_partial_keyword_match(store_db: Session, query: str):
    """
    To collect book details from book store table using partial query param.
    @param store_db: book store database instance
    @param query: partial match string
    @return: records from database
    """
    try:
        books = store_db.query(BookStore).filter(
            or_(
                BookStore.title.ilike(f"%{query}%"),
                BookStore.author.ilike(f"%{query}%"),
                BookStore.category.ilike(f"%{query}%"),
                BookStore.description.ilike(f"%{query}%")
            )
        ).all()
        logger.debug(f"Data Fetched : {books}")
        if books is None:
            logger.debug(f"Data Not Found for title {query}")
            books = JSONResponse(content={})
        return books
    except Exception as exception:
        logger.error(exception)
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=Sc.RESPONSE_MSG_500) from exception


def fetch_books_with_category(store_db: Session, category: str):
    """
    To collect book details for a particular category.
    @param store_db: book store database instance
    @param category: book category
    @return: records from database
    """
    try:
        data = store_db.query(BookStore).filter(BookStore.category == category).all()
        logger.debug(f"Data Fetched : {data}")
        if data is None:
            logger.debug(f"Data Not Found for book category {category}")
            data = JSONResponse(content={})
        return data
    except Exception as exception:
        logger.error(exception)
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=Sc.RESPONSE_MSG_500) from exception


def create_book_store(db_obj: Session, book_store_req_obj: BookCreateRequestSchema):
    """
    This method creates a new entry to book store table using the book details given as input

    :param book_store_req_obj: object of the Book request schema
    :param db_obj: instance of database
    :return: created book record object
    """
    try:
        if db_obj.query(BookStore).filter(BookStore.title == book_store_req_obj.title,
                                          BookStore.author == book_store_req_obj.author).one_or_none():
            logger.warning(f"Entry already exists with title {book_store_req_obj.title} "
                           f"and author {book_store_req_obj.author}")
            raise HTTPException(status_code=HTTP_409_CONFLICT, detail=Sc.RESPONSE_MSG_409)
        book_store_obj = BookStore(title=book_store_req_obj.title,
                                   author=book_store_req_obj.author,
                                   category=book_store_req_obj.category,
                                   description=book_store_req_obj.description)

        db_obj.add(book_store_obj)
        db_obj.commit()
        db_obj.refresh(book_store_obj)
        bookstore_obj = db_obj.query(BookStore). \
            filter(BookStore.title == book_store_obj.title,
                   BookStore.author == book_store_obj.author,
                   BookStore.category == book_store_obj.category).one_or_none()

        return bookstore_obj

    except HTTPException as ex:
        raise HTTPException(status_code=ex.status_code,
                            detail=ex.detail) from ex
    except Exception as ex:
        logger.warning(f"Unknown error {ex} has occurred while creating entry for store")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=Sc.RESPONSE_MSG_500) from ex


def update_book_store(db_obj: Session, book_id: int, book):
    """
    This method updates an existing entry in the book store table using the details given as input

    :param book_id: book id details to be updated.
    :param db_obj: instance of database
    :param book: object of book update schema.
    :return: updated book record object
    """
    try:
        db_book = db_obj.query(BookStore).filter(BookStore.id == book_id).first()
        if not db_book:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                                detail=f'Book id: {book_id} in the request is not present in the records')
        update_data = book.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_book, key, value)

        db_obj.commit()
        db_obj.refresh(db_book)
        return db_book
    except HTTPException as ex:
        raise HTTPException(status_code=ex.status_code,
                            detail=ex.detail) from ex
    except Exception as ex:
        logger.warning(f"Unknown error {ex} has occurred while creating entry for store")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=Sc.RESPONSE_MSG_500) from ex
