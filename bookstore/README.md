# BookStore App

## Overview

The BookStore app is a backend service designed to manage a collection of books. It supports creating, updating, and retrieving book details. The app provides functionalities to fetch books through various methods such as category-based search, partial query matches, and fetching all books mapped by category. The application is containerized and deployed on a Kubernetes cluster using Helm charts.

## Features

- **Create Book**: Add new books to the collection.
- **Update Book**: Modify details of existing books.
- **Fetch Books by Category**: Retrieve all books within a specific category.
- **Partial Query Search**: Search for books that partially match a query string.
- **Fetch All Books by Category**: Retrieve all books, organized by their categories.

## Prerequisites

- Docker
- Kubernetes
- Helm
- Python 3.8+
- FastAPI
- SQLAlchemy

## Setup Instructions

### Clone the Repository

```
git clone https://github.com/Sabyasachi89/BookStore.git
cd bookstore
```

### Build the Docker Image

```
bash
Copy code
docker build -t bookstore:latest .
```

### Kubernetes Deployment Using Helm

1. **Add the Helm Chart**

   Make sure you have Helm installed and initialized. Navigate to the `helm` directory where the `Chart.yaml` file is located.

   ```
   bash
   Copy code
   helm install bookstore ./helm
   ```

2. **Verify the Deployment**

   Check if the pods are running:

   ```
   bash
   Copy code
   kubectl get pods
   ```

   Check if the service is running:

   ```
   bash
   Copy code
   kubectl get services
   ```

## API Endpoints

### Create a Book

- **URL**: `/books/`

- **Method**: `POST`

- **Request Body**:

  ```
  jsonCopy code{
      "title": "Book Title",
      "author": "Author Name",
      "category": "Category Name",
      "description": "Book Description"
  }
  ```

- **Response**: `201 Created`

### Update a Book

- **URL**: `/books/{book_id}`

- **Method**: `PUT`

- **Request Body**:

  ```
  jsonCopy code{
      "title": "Updated Title",
      "author": "Updated Author",
      "description": "Updated Description",
      "category": "Updated Category"
  }
  ```

- **Response**: `200 OK` or `404 Not Found` if the book does not exist.

### Fetch Books by Category

- **URL**: `/books?category={category}`
- **Method**: `GET`
- **Response**: `200 OK` with a list of books in the specified category.

### Partial Query Search

- **URL**: `/books?query={query}`
- **Method**: `GET`
- **Response**: `200 OK` with a list of books that match the query.

### Fetch All Books by Category

- **URL**: `/books/
- **Method**: `GET`
- **Response**: `200 OK` with a list of all books organized by category.

## Configuration

### Environment Variables

- `POSTGRES_DB_NAME`: bookstore
- `POSTGRES_USER`: Database username
- `POSTGRES_PASSWORD`: Database password
- `POSTGRES_HOST`: db
- `POSTGRES_PORT`: 5432
- `DB_TYPE`: postgresql
- `LOG_LEVEL`: DEBUG
- `POOL_RECYCLE`: 1200
- `DB_POOL_SIZE`: 250
- `DB_MAX_OVERFLOW`: 100
- `MODULE_NAME`: BOOKSTORE
- `BASE_URL`: /books

### Helm Values

You can customize the Helm chart by modifying the `values.yaml` file located in the `helm` directory.

## Development

### Setting Up the Development Environment

1. **Navigate to the project folder.**

2. **Install Dependencies**

   ```
   bash
   Copy code
   pipenv install --dev
   ```

3. **Activate the virtual environment**

   ```
   bash
   pipenv shell
   ```

4. **Run the Application**

   ```
   bash
   uvicorn app.src.main:app --reload --port 8000 --host 0.0.0.0
   ```

5. **Access the application**

   ```
   Open your browser and go to `http://localhost:8000/books
   ```

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Create a new Pull Request.

## Contact

For any inquiries or feedback, please contact [saachii89@gmail.com].