# Multilingual FAQ System

A robust backend system for managing FAQs with multilingual support, WYSIWYG editor compatibility, and efficient caching.

## Features

- REST API for FAQ management
- Multilingual support (English, Hindi, Bengali)
- Automatic translation using Google Cloud Translation API
- Redis caching for improved performance
- HTML sanitization for rich text content
- Rate limiting and security measures
- Comprehensive error handling and logging
- Database migrations and Row Level Security

## Tech Stack

- **Django** & **Django REST Framework**
- **Redis** for caching
- **Google Cloud Translation API** for multilingual support
- **django-ckeditor** for WYSIWYG editor
- **pytest** for testing
- **flake8** for Python linting
- **docker-compose** for containerized deployment

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- Redis server
- Docker and Docker Compose 
- Git (optional, for version control)

## Installation

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone <https://github.com/hemankpatwal/bharatfd-faq-backend/tree/main/faq_project/faq>
   cd faq-backend
   ```

### Install dependencies:

```bash
pip install -r requirements.txt
```

### Set up environment variables by creating a .env file with the following content:

```bash
DJANGO_SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
REDIS_URL=redis://localhost:6379
GOOGLE_API_KEY=your_google_api_key
LANGUAGES=en,hi,bn
```
### Set up Redis:

Start Redis server locally:

```bash
redis-server
```

### Run database migrations:

```bash
python manage.py migrate
```

### Start the development server:

```bash
python manage.py runserver
```

### Docker Setup:
Ensure Docker and Docker Compose are installed.

Create a .env file as described above.

Build and start the containers:

```bash
docker-compose up -d
```

## API Endpoints
### Get All FAQs
```bash
GET /api/faqs
GET /api/faqs?lang=hi # Hindi
GET /api/faqs?lang=bn # Bengali
```

### Get FAQ by ID
```bash 
GET /api/faqs/:id
GET /api/faqs/:id?lang=hi
```

### Create FAQ
```bash
POST /api/faqs
{
  "question": "What is this?",
  "answer": "<p>This is a FAQ system.</p>"
}
```

### Update FAQ
```bash
PUT /api/faqs/:id
{
  "question": "Updated question",
  "answer": "<p>Updated answer</p>"
}
```

### Delete FAQ
```bash
DELETE /api/faqs/:id
```

## Testing
### Run the test suite:

```bash
pytest
```

### Run tests with coverage:

```bash
pytest --cov=faq_manager
```

## evelopment Scripts
-`python manage.py runserver`: Start development server
-`python manage.py test`: Run test suite
-`flake8 .`: Run Python linter