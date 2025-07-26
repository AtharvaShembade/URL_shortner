# Python URL Shortener

A simple, rate-limited URL shortener built with Flask and SQLite.

## Features

- Shorten long URLs to easy-to-share short codes
- Redirect short codes to the original URLs
- Rate limiting to prevent abuse (configurable)
- Input validation for URLs
- Error pages for 404 (not found) and 429 (rate limit exceeded)
- Clean, responsive UI with Tailwind CSS

## Requirements

- Python 3.7+
- Flask
- Flask-Limiter

## Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/url-shortener.git
    cd url-shortener
    ```

2. **Run the application:**
    ```bash
    python app.py
    ```