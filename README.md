# Travli Location API

Location and geocoding microservice for **Travli**.

This service provides destination search functionality using **Geoapify** as the external geocoding provider and **Redis** as a cache to reduce external API requests and improve response times.

## Architecture

```text
                  ┌─────────────────────┐
                  │ Travli Location API │
                  │      FastAPI        │
                  └──────┬────────┬─────┘
                         │        │
                    Cache hit     │ Cache miss
                         │        ▼
                         │   ┌───────────┐
                         │   │ Geoapify  │
                         │   └───────────┘
                         │        │
                         │        ▼
                         │   Store result
                         │        │
                         ▼        ▼
                       ┌──────────────┐
                       │    Redis     │
                       │   TTL: 1h    │
                       └──────────────┘
```

## Features

* City and destination search
* Geocoding through Geoapify
* Normalized API responses
* Redis caching
* 1-hour cache expiration
* REST API with FastAPI
* Automatic OpenAPI documentation
* Unit and integration tests
* Docker support

## Technology Stack

* Python 3.12
* FastAPI
* Pydantic
* HTTPX
* Redis
* Geoapify Geocoding API
* pytest
* uv
* Docker

## Project Structure

```text
Travli-location-api/
├── app/
│   ├── api/
│   │   └── routes/
│   │       └── locations.py
│   ├── cache/
│   │   └── redis.py
│   ├── providers/
│   │   └── geoapify.py
│   ├── schemas/
│   │   └── location.py
│   ├── services/
│   │   └── location_service.py
│   ├── config.py
│   └── main.py
│
├── tests/
│   ├── test_health.py
│   ├── test_locations.py
│   ├── test_location_service.py
│   ├── test_geoapify.py
│   └── test_redis.py
│
├── insomnia/
│   └── Travli-location-api.json
│
├── .env.example
├── .gitignore
├── Dockerfile
├── pyproject.toml
└── README.md
```

## Requirements

* Python 3.12
* uv
* Docker
* A Geoapify API key
* Travli Location Redis instance

## Configuration

Create a `.env` file based on `.env.example`:

```env
APP_NAME=Travli-location-api
APP_ENV=development
PORT=8000

GEOAPIFY_API_KEY=your_api_key

REDIS_URL=redis://localhost:6380
REDIS_TTL=3600
```

### Environment variables

| Variable           | Description               | Default                  |
| ------------------ | ------------------------- | ------------------------ |
| `APP_NAME`         | Application name          | `Travli-location-api`     |
| `APP_ENV`          | Application environment   | `development`            |
| `PORT`             | API port                  | `8000`                   |
| `GEOAPIFY_API_KEY` | Geoapify API key          | —                        |
| `REDIS_URL`        | Redis connection URL      | `redis://localhost:6380` |
| `REDIS_TTL`        | Cache lifetime in seconds | `3600`                   |

The `.env` file must not be committed to the repository.

## Installation

Install the project dependencies with:

```bash
uv sync
```

## Running locally

Make sure the Travli infrastructure is running and that the Location Redis instance is available on port `6380`.

Start the API with:

```bash
uv run uvicorn app.main:app --reload --port 8000
```

The API will be available at:

```text
http://localhost:8000
```

## API Documentation

FastAPI automatically exposes interactive API documentation.

Swagger UI:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

## API Endpoints

### Health check

```http
GET /health
```

Example response:

```json
{
  "status": "ok"
}
```

### Search locations

```http
GET /api/v1/locations/search?q={query}
```

Example:

```http
GET /api/v1/locations/search?q=Bilbao
```

Example response:

```json
{
  "results": [
    {
      "name": "Bilbao",
      "country": "Spain",
      "country_code": "es",
      "latitude": 43.263,
      "longitude": -2.935
    }
  ]
}
```

The API exposes its own normalized response instead of returning the raw Geoapify response.

## Caching

Location searches are cached in Redis.

The cache key follows this format:

```text
location:search:{query}
```

For example:

```text
location:search:bilbao
```

Cached results expire after one hour by default:

```text
REDIS_TTL=3600
```

The request flow is:

```text
Request
   │
   ▼
Redis
   │
   ├── Cache hit ──────► Return cached result
   │
   └── Cache miss
            │
            ▼
         Geoapify
            │
            ▼
       Store in Redis
            │
            ▼
       Return result
```

## Testing

Run the complete test suite with:

```bash
uv run pytest
```

The tests cover:

* Health endpoint
* Location search endpoint
* Query validation
* Location service
* Cache hit and cache miss behaviour
* Geoapify provider
* Redis cache

External services are mocked during testing, so the test suite does not require requests to Geoapify or a running Redis instance.

## Docker

Build the image:

```bash
docker build -t Travli-location-api .
```

Run the container:

```bash
docker run --rm \
  --env-file .env \
  -p 8000:8000 \
  Travli-location-api
```

When running the API inside Docker, `REDIS_URL` must point to the Redis service reachable from the container rather than `localhost`.

## Insomnia

An Insomnia export is included in:

```text
insomnia/Travli-location-api.json
```

Import this file into Insomnia to obtain the predefined requests:

```text
Travli Location API
├── Health
└── Search Location
```

The default environment uses:

```text
base_url = http://localhost:8000
```

## External Services

### Geoapify

Geoapify is used as the external geocoding provider.

The API key is configured through:

```env
GEOAPIFY_API_KEY=your_api_key
```

The application isolates the external provider inside:

```text
app/providers/geoapify.py
```

This keeps the rest of the application independent from the provider implementation.

## Development

Run the application:

```bash
uv run uvicorn app.main:app --reload --port 8000
```

Run tests:

```bash
uv run pytest
```

Run Ruff:

```bash
uv run ruff check .
```
