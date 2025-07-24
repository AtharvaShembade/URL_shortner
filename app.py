from flask import Flask, render_template, request, redirect, abort, g
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from models import init_db_programmatically, get_db, close_connection
from utils import generate_short_code, is_valid_url

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits = ["200 per day", "50 per hour"],
    storage_uri = "memory://",
)

app.teardown_appcontext(close_connection)

#web routes

@app.route("/", methods = ["GET", "POST"])
@limiter.limit("10 per minute")
def index():
    if request.method == "POST":
        original_url = request.form["url"]

        if not is_valid_url(original_url):
            return render_template("index.html", error = "Please enter a valid URL (e.g., https://example.com)."), 400

        db = get_db()
        fetch = db.execute('SELECT short_code FROM urls WHERE original_url = ?', (original_url,))
        existing = fetch.fetchone()

        if existing:
            short_code = existing['short_code']
        else:
            short_code = generate_short_code()
            db.execute('INSERT INTO urls (original_url, short_code) VALUES (?, ?)',
                        (original_url, short_code))
            db.commit()

        short_url = request.url + short_code
        return render_template("index.html", short_url = short_url)

    return render_template("index.html")



@app.route("/<string:short_code>")
def redirect_to_original_url(short_code):

    db = get_db()
    fetch = db.execute('SELECT original_url FROM urls WHERE short_code = ?', (short_code,))
    url_record = fetch.fetchone()

    if url_record:
        return redirect(url_record['original_url'])
    else:
        abort(404)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(429)
def rate_limit_exceeded(e):
    return render_template('429.html', error_description=e.description), 429


if __name__ == "__main__":
    init_db_programmatically()
    app.run(debug=True)