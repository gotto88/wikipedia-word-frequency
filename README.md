# Wikipedia Word Frequency API

Implementation of an API calculating word frequency for a given Wikipedia page and pages linked to it.
For details of the technical solution, status and future steps check `project_summary.txt`

## Features

- **Multi-threaded Page Fetching**: Configurable number of threads for paralell fetching of pages
- **Configurable Depth**: Fetch linked pages up to a specified depth
- **Word Frequency Analysis**: Calculate word counts and percentages across multiple pages
- **Filtering Options**: Ignore specific words and apply percentile thresholds

**Note**: Wikipedia has limitations for number of page fetching in a time window. Using to much threads can lead to rejections!

## API Endpoints

### Root Endpoint
- **GET** `/` - Health check endpoint, returns 200 OK

### Word Frequency
- **GET** `/word-frequency?article={page_name}&depth={depth}` - Calculate word frequencies for a page and its links

### Keywords
- **POST** `/keywords` - Calculate word frequencies with additional filtering options
  ```json
  {
    "article": "Python (programming language)",
    "depth": 2,
    "ignore_list": ["the", "and", "or"],
    "percentile": 5
  }
  ```

## Quick Start

### Prerequisites
- Python 3.11+
- Docker and Docker Compose

### Development Environment

```bash
# Clone the repository
git clone <repository-url>
cd wikipedia-word-frequency

# Start the API with development settings (auto-reload enabled)
docker-compose up --build -d

# The API will be available at http://localhost:8000
# API documentation at http://localhost:8000/docs
```

### Production Environment

```bash
# Start the API with production settings
docker-compose -f docker-compose.prod.yml up --build -d

# Check logs
docker-compose -f docker-compose.prod.yml logs -f
```

## Docker Configuration

### Development (`docker-compose.yml`)
- **Threads**: 10 concurrent threads for page fetching
- **Features**: Hot reload, source code mounting, DEBUG logging
- **Container Name**: `word-frequency-api-dev`
- **Command**: Uses uvicorn with `--reload` for development

### Production (`docker-compose.prod.yml`)
- **Threads**: 10 concurrent threads for page fetching
- **Features**: Production optimized, resource limits, INFO logging
- **Container Name**: `word-frequency-api-prod`


## Environment Variables

- `MAX_FETCHING_THREADS`: Maximum number of threads for concurrent page fetching (set to 10)
- `PYTHONDONTWRITEBYTECODE`: Prevents Python from writing .pyc files
- `PYTHONUNBUFFERED`: Ensures Python output is sent straight to terminal
- `PYTHONPATH`: Sets the Python path to `/app`
- `LOG_LEVEL`: Logging level (DEBUG for dev, INFO for prod)
- `CACHE_TTL`: The ttl of in-memory cache
- `USE_CACHE`: Sets if cache is used


# Production
docker-compose -f docker-compose.prod.yml up --build -d
docker-compose -f docker-compose.prod.yml logs -f
docker-compose -f docker-compose.prod.yml down

# Rebuild without cache
docker-compose build --no-cache
docker-compose -f docker-compose.prod.yml build --no-cache
```

## Testing

```bash
# Run tests
cd test
python -m pytest test_page_handler.py -v
python -m pytest test_wikipage_fetcher.py -v
```

## Health Check

The container includes a health check that pings the root endpoint (`/`) every 30 seconds to ensure the API is responding correctly.

## Network

Each environment uses its own custom bridge network for isolation and security.

## Troubleshooting

