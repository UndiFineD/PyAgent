# API Documentation - impl_000494

## Base URL
`/api/impl_000494`

## Endpoints

### GET /impl_000494
**Description:** Retrieve data for impl_000494

**Response:**
```json
{
  "status": "success",
  "data": {
    "archetype": "resilience",
    "component": "component_50_4"
  }
}
```

### POST /impl_000494
**Description:** Create new resource

**Request Body:**
```json
{
  "name": "string",
  "value": "number"
}
```

**Response:**
```json
{
  "id": "string",
  "created": true,
  "timestamp": "2026-04-06T07:00:00Z"
}
```

### Error Handling
All endpoints return HTTP status codes:
- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 500: Internal Server Error

## Rate Limiting
- 100 requests per minute per IP
- Headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`

## Authentication
Requests require `Authorization: Bearer <token>`

## Versioning
Current API Version: 1.0.0
