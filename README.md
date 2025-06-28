# Book Review API

A FastAPI-based backend for managing books and reviews, with SQLite database, Redis caching, and comprehensive testing.

## Features

- **CRUD Operations**: Create and retrieve books and reviews
- **Redis Caching**: Automatic caching for improved performance
- **SQLite Database**: Lightweight, file-based database
- **Comprehensive Testing**: Unit and integration tests
- **Async Support**: Full async/await support throughout
- **Error Handling**: Proper HTTP status codes and error messages

## Tech Stack

- **FastAPI**: Modern, fast web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **SQLite**: Lightweight database
- **Redis**: In-memory caching
- **Pydantic**: Data validation
- **Pytest**: Testing framework

## Prerequisites

- Python 3.8+
- Redis server (for caching)
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Book-Review
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   .\venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   DATABASE_URL=sqlite+aiosqlite:///./bookreview.db
   REDIS_URL=redis://localhost:6379/0
   ```

## Database Setup

### Option 1: Automatic Table Creation (Recommended)
The application automatically creates database tables on startup. No manual migration needed.

### Option 2: Manual Table Creation
If you prefer manual control:
```bash
python -m app.create_tables
```

## Running Redis

### Using Docker (Recommended)
```bash
docker run -p 6379:6379 redis
```

### Using Windows
Download and install [Memurai](https://www.memurai.com/download) (Redis-compatible for Windows)

### Using macOS
```bash
brew install redis
redis-server
```

## Running the Application

### Development Mode
```bash
uvicorn app.main:app --reload
```

### Production Mode
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Books
- `GET /books` - Get all books with reviews
- `POST /books` - Create a new book

### Reviews
- `GET /books/{book_id}/reviews` - Get reviews for a specific book
- `POST /books/{book_id}/reviews` - Add a review to a book

### Example Usage

#### Create a Book
```bash
curl -X POST "http://localhost:8000/books/" \
     -H "Content-Type: application/json" \
     -d '{"title": "Clean Code", "author": "Robert C. Martin"}'
```

#### Get All Books
```bash
curl "http://localhost:8000/books/"
```

#### Add a Review
```bash
curl -X POST "http://localhost:8000/books/1/reviews" \
     -H "Content-Type: application/json" \
     -d '{"review_text": "Excellent book!", "rating": 5}'
```

#### Get Book Reviews
```bash
curl "http://localhost:8000/books/1/reviews"
```

## Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_books.py

# Run tests with coverage
pytest --cov=app
```

### Test Structure
- **Unit Tests**: Mock service functions to test endpoint logic
- **Integration Tests**: Test cache-miss scenarios with real database
- **Cache Tests**: Verify Redis integration and fallback behavior

### Test Files
- `tests/test_books.py` - Book endpoint and Review endpoint tests
- `tests/test_cache.py` - Cache integration tests

## Project Structure

```
Book-Review/
├── app/
│   ├── models/          # SQLAlchemy models
│   │   ├── book.py
│   │   └── review.py
│   ├── schemas/         # Pydantic schemas
│   │   ├── book.py
│   │   └── review.py
│   ├── routes/          # FastAPI routers
│   │   └── books.py
│   ├── services/        # Business logic
│   │   └── book_service.py
│   ├── cache/           # Redis integration
│   │   └── redis_cache.py
│   ├── db.py            # Database configuration
│   ├── db_base.py       # SQLAlchemy Base
│   └── main.py          # FastAPI application
├── tests/               # Test files
│   ├── test_books.py
│   ├── test_reviews.py
│   └── test_cache.py
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables
└── README.md           # This file
```

## Caching Strategy

- **GET /books**: Cached with key `books:list`
- **GET /books/{id}/reviews**: Cached with key `book:{id}:reviews`
- **Cache Invalidation**: Automatically invalidated on POST operations
- **Fallback**: Database fallback if Redis is unavailable

## Error Handling

- **404 Not Found**: Book or reviews not found
- **503 Service Unavailable**: Redis cache unavailable (with DB fallback)
- **422 Validation Error**: Invalid request data
- **500 Internal Server Error**: Unexpected server errors

## Development

### Adding New Endpoints
1. Add service function in `app/services/book_service.py`
2. Add route in `app/routes/books.py`
3. Add Pydantic schemas in `app/schemas/`
4. Write tests in `tests/`

### Adding New Models
1. Create model in `app/models/`
2. Add to `app/db_base.py` imports
3. Update `app/main.py` startup event
4. Add corresponding schemas and tests

## Troubleshooting

### Common Issues

1. **Redis Connection Error**
   - Ensure Redis is running: `docker run -p 6379:6379 redis`
   - Check REDIS_URL in `.env` file

2. **Database Errors**
   - Delete `bookreview.db` file and restart the application
   - Check DATABASE_URL in `.env` file

3. **Import Errors**
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt`

4. **Test Failures**
   - Ensure Redis is running for cache tests
   - Clear database before running integration tests

### Logs
The application logs cache hits/misses and database operations. Check the console output for debugging information.
