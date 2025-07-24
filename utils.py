import string
import random
from urllib.parse import urlparse
from models import get_db

def generate_short_code(length=7):
    characters = string.ascii_letters + string.digits
    while True:
        short_code = ''.join(random.choice(characters) for _ in range(length))

        db = get_db()
        fetch = db.execute('SELECT short_code FROM urls WHERE short_code = ?', (short_code,))
        if fetch.fetchone() is None:
            return short_code


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except (ValueError, AttributeError):
        return False