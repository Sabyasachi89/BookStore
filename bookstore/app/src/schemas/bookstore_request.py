from pydantic import BaseModel
from typing import Optional
from app.src.constants import StoreConstants


class BookCreate(BaseModel):
    title: str
    author: str
    category: str
    description: str

    # pylint: disable=R0903
    class Config(object):
        """For discarding extra fields"""
        extra = StoreConstants.FORBID_STR


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None

    class Config(object):
        """For discarding extra fields"""
        extra = StoreConstants.FORBID_STR
