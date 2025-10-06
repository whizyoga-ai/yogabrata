# API Documentation

## Overview

The Yogabrata API is built with FastAPI and provides endpoints for managing yoga classes, instructors, bookings, and user accounts.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

Currently, the API uses simple token-based authentication. Include the token in the Authorization header:

```
Authorization: Bearer your-token-here
```

## Endpoints

### Health Check

**GET** `/health`

Returns the health status of the API.

**Response:**
```json
{
  "status": "healthy",
  "service": "yogabrata-api",
  "version": "1.0.0"
}
```

### Classes

**GET** `/api/v1/classes`

Get all available yoga classes.

**Response:**
```json
{
  "classes": [
    {
      "id": 1,
      "name": "Hatha Yoga",
      "instructor": "Sarah Johnson",
      "duration": 60,
      "capacity": 20,
      "description": "Traditional hatha yoga practice"
    }
  ]
}
```

**GET** `/api/v1/classes/{class_id}`

Get a specific class by ID.

**Parameters:**
- `class_id` (integer): The class ID

**Response:**
```json
{
  "id": 1,
  "name": "Hatha Yoga",
  "instructor": "Sarah Johnson",
  "duration": 60,
  "capacity": 20,
  "description": "Traditional hatha yoga practice",
  "schedule": "Monday, Wednesday, Friday 9:00 AM"
}
```

### Instructors

**GET** `/api/v1/instructors`

Get all instructors.

**Response:**
```json
{
  "instructors": [
    {
      "id": 1,
      "name": "Sarah Johnson",
      "specialties": ["Hatha", "Meditation"],
      "experience_years": 8,
      "bio": "Experienced yoga instructor specializing in traditional hatha yoga"
    }
  ]
}
```

**GET** `/api/v1/instructors/{instructor_id}`

Get a specific instructor by ID.

**Parameters:**
- `instructor_id` (integer): The instructor ID

## Error Handling

The API uses standard HTTP status codes:

- `200` - Success
- `400` - Bad Request
- `401` - Unauthorized
- `404` - Not Found
- `500` - Internal Server Error

Error response format:
```json
{
  "detail": "Error description",
  "error_code": "ERROR_CODE"
}
```

## Rate Limiting

The API implements rate limiting to ensure fair usage:

- Frontend routes: 30 requests per second
- API routes: 10 requests per second

## CORS

The API allows cross-origin requests from:
- `http://localhost:3000` (development)
- `https://yogabrata.com` (production)

## SDKs and Libraries

### JavaScript/TypeScript
```javascript
// Example using fetch
const response = await fetch('http://localhost:8000/api/v1/classes');
const data = await response.json();
```

### Python
```python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.get('http://localhost:8000/api/v1/classes')
    data = response.json()
```

## Webhooks

The API supports webhooks for real-time notifications. Register a webhook URL to receive notifications about:

- Class schedule changes
- New bookings
- Instructor updates

## Support

For API support or questions, please contact our development team or create an issue in the GitHub repository.
