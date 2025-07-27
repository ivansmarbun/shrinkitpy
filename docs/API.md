# API Documentation

ShrinkItPy provides both web interface and RESTful API endpoints for URL shortening and analytics.

## Base URL
- **Development**: `http://localhost:5000`
- **Production**: `https://your-domain.com`

## Authentication
Currently, no authentication is required for API endpoints. This may change in future versions.

## Content-Type
All API requests should use `Content-Type: application/json` for POST requests.

---

## Endpoints

### 1. Shorten URL

Create a shortened URL from a long URL.

**Endpoint**: `POST /shorten`

**Request Body**:
```json
{
  "url": "https://example.com/very/long/url/that/needs/shortening"
}
```

**Response** (200 OK):
```json
{
  "short_url": "http://localhost:5000/s/abc123",
  "short_id": "abc123",
  "long_url": "https://example.com/very/long/url/that/needs/shortening"
}
```

**Error Response** (400 Bad Request):
```json
{
  "error": "Missing URL"
}
```

**cURL Example**:
```bash
curl -X POST http://localhost:5000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

---

### 2. Redirect Short URL

Redirect a short URL to its original destination.

**Endpoint**: `GET /s/{short_id}`

**Parameters**:
- `short_id` (string): The unique identifier for the shortened URL

**Response**: 
- **302 Found**: Redirects to the original URL
- **404 Not Found**: If the short ID doesn't exist

**Example**:
```bash
curl -L http://localhost:5000/s/abc123
# Redirects to the original URL
```

**Error Response** (404 Not Found):
```html
<!DOCTYPE html>
<html>
<head><title>404 Not Found</title></head>
<body><h1>URL not found</h1></body>
</html>
```

---

### 3. Get URL Analytics

Retrieve analytics information for a shortened URL.

**Endpoint**: `POST /analytics`

**Request Body**:
```json
{
  "short_url": "abc123"
}
```
*Note: You can provide either the full short URL or just the short_id*

**Response** (200 OK):
```json
{
  "short_id": "abc123",
  "long_url": "https://example.com/very/long/url",
  "created_at": "2025-07-27T10:30:45.123456"
}
```

**Error Response** (400 Bad Request):
```json
{
  "error": "Missing short_url"
}
```

**Error Response** (404 Not Found):
```json
{
  "error": "URL not found"
}
```

**cURL Example**:
```bash
curl -X POST http://localhost:5000/analytics \
  -H "Content-Type: application/json" \
  -d '{"short_url": "abc123"}'
```

---

## Web Interface Endpoints

### 1. Home Page

**Endpoint**: `GET /`

Returns the main page with URL shortening form.

**Response**: HTML page with form interface

---

### 2. Create Short URL (Web Form)

**Endpoint**: `POST /`

**Form Data**:
- `url`: The long URL to shorten

**Response**: HTML page showing the shortened URL

---

### 3. Analytics Page

**Endpoint**: `GET /analytics`

Returns the analytics page with form to check URL statistics.

**Response**: HTML page with analytics form

---

## Response Codes

| Code | Description |
|------|-------------|
| 200  | Success |
| 302  | Redirect (for short URL access) |
| 400  | Bad Request (missing or invalid parameters) |
| 404  | Not Found (URL doesn't exist) |
| 500  | Internal Server Error |

---

## Rate Limiting

Currently, no rate limiting is implemented. This may be added in future versions for production use.

---

## Examples

### Python Example

```python
import requests
import json

# Shorten a URL
def shorten_url(long_url, base_url="http://localhost:5000"):
    response = requests.post(
        f"{base_url}/shorten",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"url": long_url})
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Get analytics
def get_analytics(short_id, base_url="http://localhost:5000"):
    response = requests.post(
        f"{base_url}/analytics",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"short_url": short_id})
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Usage
result = shorten_url("https://example.com/very/long/url")
if result:
    print(f"Short URL: {result['short_url']}")
    
    # Get analytics for the shortened URL
    analytics = get_analytics(result['short_id'])
    if analytics:
        print(f"Created: {analytics['created_at']}")
```

### JavaScript Example

```javascript
// Shorten URL
async function shortenUrl(longUrl) {
    try {
        const response = await fetch('/shorten', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: longUrl })
        });
        
        if (response.ok) {
            return await response.json();
        } else {
            const error = await response.json();
            console.error('Error:', error);
            return null;
        }
    } catch (error) {
        console.error('Network error:', error);
        return null;
    }
}

// Get analytics
async function getAnalytics(shortId) {
    try {
        const response = await fetch('/analytics', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ short_url: shortId })
        });
        
        if (response.ok) {
            return await response.json();
        } else {
            const error = await response.json();
            console.error('Error:', error);
            return null;
        }
    } catch (error) {
        console.error('Network error:', error);
        return null;
    }
}

// Usage
shortenUrl('https://example.com/long/url')
    .then(result => {
        if (result) {
            console.log('Short URL:', result.short_url);
            
            // Get analytics
            return getAnalytics(result.short_id);
        }
    })
    .then(analytics => {
        if (analytics) {
            console.log('Created:', analytics.created_at);
        }
    });
```

---

## Error Handling

All API endpoints return appropriate HTTP status codes and error messages in JSON format (for API endpoints) or HTML format (for web endpoints).

### Common Error Patterns:

1. **Missing Required Fields**:
   ```json
   {
     "error": "Missing URL"
   }
   ```

2. **Resource Not Found**:
   ```json
   {
     "error": "URL not found"
   }
   ```

3. **Invalid URL Format**:
   ```json
   {
     "error": "Invalid URL format"
   }
   ```

---

## Future API Enhancements

Planned features for future versions:

1. **Authentication**: API key or JWT token authentication
2. **Rate Limiting**: Request throttling per IP/user
3. **Custom Short IDs**: Allow users to specify custom short identifiers
4. **Bulk Operations**: Shorten multiple URLs in one request
5. **Analytics Extensions**: Click tracking, geographic data, referrer information
6. **URL Expiration**: Set expiration dates for shortened URLs
7. **QR Code Generation**: Generate QR codes for shortened URLs

---

## Changelog

### v1.0 (Current)
- Basic URL shortening
- URL redirection
- Simple analytics
- Web interface

### Planned v1.1
- Enhanced analytics with click tracking
- API authentication
- Rate limiting
