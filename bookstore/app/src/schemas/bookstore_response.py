from pydantic import BaseModel, Field
from typing import List

RESPONSE_MSG = 'Resource created successfully'
UPDATE_MSG = 'Resource updated successfully'


class Book(BaseModel):
    id: int
    title: str
    author: str
    description: str

    class Config:
        orm_mode = True


class CategoryBooks(BaseModel):
    category: str
    books: List[Book]


class BookStore(BaseModel):
    """
        contains details of all the key parameter of the response json
    """
    id: int = Field(alias='id')
    title: str = Field(alias='title')
    author: str = Field(alias='author')
    category: str = Field(alias='category')
    description: str = Field(alias='description')

    class Config(object):
        """Maintain ORM mode"""
        orm_mode = True
        allow_population_by_field_name = True


class RegistryResponse(BaseModel):
    """Class for parameter of the response json"""
    id: int
    message: str = RESPONSE_MSG

    class Config(object):
        """Maintain ORM mode"""
        orm_mode = True
        allow_population_by_field_name = True


class UpdateResponse(BaseModel):
    """Class for parameter of the response json"""
    id: int
    message: str = UPDATE_MSG

    class Config(object):
        """Maintain ORM mode"""
        orm_mode = True
        allow_population_by_field_name = True
