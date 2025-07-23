# ShrinkitPy URL Shortener

This is a Flask-based URL shortener with analytics and SQLite database storage. The project uses a modular structure for maintainability.

## Features
- Shorten long URLs via web form or API
- Redirect short URLs to their original destination
- View analytics for short URLs via web form or API
- Persistent storage using SQLite

## Project Structure
- `app.py`: Main Flask app and routes
- `services/`: Contains database and URL logic
- `templates/`: HTML templates for web forms

## Getting Started
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the app:
   ```bash
   python app.py
   ```
3. Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser

## Usage
- **Shorten URL:** Use the form on the homepage or POST to `/shorten` with JSON `{ "url": "LONG_URL" }`
- **Redirect:** Access `/s/SHORT_ID` to be redirected
- **Analytics:** Use the form at `/analytics` or POST to `/analytics` with JSON `{ "short_url": "SHORT_URL" }`

## Example curl
```
curl -X POST -H "Content-Type: application/json" \
    -d '{"short_url": "http://localhost:5000/s/fOVDMX"}' \
    http://localhost:5000/analytics
```
