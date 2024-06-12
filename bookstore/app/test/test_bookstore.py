import pytest
from os import path, getcwd
from datetime import datetime as time
import sys
from fastapi.testclient import TestClient
from starlette import status
from db.src.seed import seed
from app.src.main import app, prefix_link
from app.src.database import get_db

print("current working directory: " + str(getcwd()))
sys.path.append(path.abspath('/usr/src/app/src'))

sys._called_from_test = True
expectedTestTimeDuration = 1000000

global_store_id = 0

app.dependency_overrides[get_db] = get_db

client = TestClient(app)


@pytest.fixture(scope="function")
def db():
    seed()


def test_case_1_get_all_books_(db):
    """ fetch all the books """
    start_time = time.utcnow()
    response = client.get(f"{prefix_link}")
    end_time = time.utcnow()
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
    {
        "category": "Drama",
        "books": [
            {
                "id": 1,
                "title": "The Lion",
                "author": "Peter",
                "description": "drama movie"
            },
            {
                "id": 3,
                "title": "Devdas",
                "author": "Sarat",
                "description": "romantic drama"
            }
        ]
    },
    {
        "category": "Mythology",
        "books": [
            {
                "id": 2,
                "title": "Ramayana",
                "author": "Modi",
                "description": "indian mythology"
            }
        ]
    }
    ]

    duration = end_time - start_time
    duration = duration.microseconds
    assert duration <= expectedTestTimeDuration
    print(f"Response duration : {duration / 10000000} Sec")


def test_case_2_get_books_by_category(db):
    """ fetch all the books """
    start_time = time.utcnow()
    response = client.get(f"{prefix_link}?category=Drama")
    end_time = time.utcnow()
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "id": 1,
            "title": "The Lion",
            "author": "Peter",
            "category": "Drama",
            "description": "drama movie"
        },
        {
            "id": 3,
            "title": "Devdas",
            "author": "Sarat",
            "category": "Drama",
            "description": "romantic drama"
        }
    ]
    duration = end_time - start_time
    duration = duration.microseconds
    assert duration <= expectedTestTimeDuration
    print(f"Response duration : {duration / 10000000} Sec")


def test_case_3_get_book_details_by_partial_match(db):
    """ fetch all the books """
    start_time = time.utcnow()
    response = client.get(f"{prefix_link}?query=dev")
    end_time = time.utcnow()
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
    {
        "id": 3,
        "title": "Devdas",
        "author": "Sarat",
        "category": "Drama",
        "description": "romantic drama"
    }
    ]
    duration = end_time - start_time
    duration = duration.microseconds
    assert duration <= expectedTestTimeDuration
    print(f"Response duration : {duration / 10000000} Sec")


def test_case_4_invalid_request_parameter(db):
    """ fetch all the books """
    start_time = time.utcnow()
    response = client.get(f"{prefix_link}?name=dev")
    print(response)
    end_time = time.utcnow()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
    "detail": {
        "error": {
            "message": "Invalid query parameter: name"
        }
    }
    }
    duration = end_time - start_time
    duration = duration.microseconds
    assert duration <= expectedTestTimeDuration
    print(f"Response duration : {duration / 10000000} Sec")


def test_case_5_category_not_present_in_database(db):
    """ fetch all the books """
    start_time = time.utcnow()
    response = client.get(f"{prefix_link}?category=abc")
    print(response)
    end_time = time.utcnow()
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
    duration = end_time - start_time
    duration = duration.microseconds
    assert duration <= expectedTestTimeDuration
    print(f"Response duration : {duration / 10000000} Sec")


def test_case_6_method_not_allowed(db):
    """ validate invalid end point error response """
    start_time = time.utcnow()
    response = client.get(f"{prefix_link}/a/?category=abc")
    print(response)
    end_time = time.utcnow()
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert response.json() == {
        "detail": {
            "error": {
                "message": "Method Not Allowed"
            }
        }
    }
    duration = end_time - start_time
    duration = duration.microseconds
    assert duration <= expectedTestTimeDuration
    print(f"Response duration : {duration / 10000000} Sec")


def test_case_7_invalid_endpoint(db):
    """ validate invalid end point error response """
    start_time = time.utcnow()
    response = client.get(f"http://127.0.0.1:8000/a/books/?category=Drama")
    print(response)
    end_time = time.utcnow()
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": {
            "error": {
                "message": "Not Found"
            }
        }
    }
    duration = end_time - start_time
    duration = duration.microseconds
    assert duration <= expectedTestTimeDuration
    print(f"Response duration : {duration / 10000000} Sec")


def test_case_8_successful_creation(db):
    """ validate invalid end point error response """
    start_time = time.utcnow()
    body = {
        "title": "the hobbit",
        "author": "david",
        "category": "Thriller",
        "description": "thriller and drama"
    }
    response = client.post(url=f'{prefix_link}',headers={'Content-Type':'application/json'},json=body)
    print('post response:',response)
    end_time = time.utcnow()
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "id": 4,
        "message": "Resource created successfully"
    }
    duration = end_time - start_time
    duration = duration.microseconds
    assert duration <= expectedTestTimeDuration
    print(f"Response duration : {duration / 10000000} Sec")


def test_case_9_update_existing_record(db):
    """ validate successful update"""
    start_time = time.utcnow()
    body = {
        "title": "the final update",
        "author": "stewart",
        "category": "Thriller",
        "description": "thriller and action"
    }
    response = client.put(url=f'{prefix_link}/2',headers={'Content-Type':'application/json'},json=body)
    end_time = time.utcnow()
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 2,
        "message": "Resource updated successfully"
    }
    duration = end_time - start_time
    duration = duration.microseconds
    assert duration <= expectedTestTimeDuration
    print(f"Response duration : {duration / 10000000} Sec")


def test_case_10_update_non_existing_record(db):
    """ validate not found error"""
    start_time = time.utcnow()
    body = {
        "title": "the hobbit",
        "author": "stewart",
        "category": "Thriller",
        "description": "thriller and action"
    }
    response = client.put(url=f'{prefix_link}/8',headers={'Content-Type':'application/json'},json=body)
    end_time = time.utcnow()
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": {
            "error": {
                "message": "Book id: 8 in the request is not present in the records"
            }
        }
    }
    duration = end_time - start_time
    duration = duration.microseconds
    assert duration <= expectedTestTimeDuration
    print(f"Response duration : {duration / 10000000} Sec")
