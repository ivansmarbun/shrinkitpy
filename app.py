from flask import Flask, request, jsonify, redirect, render_template
from utils.utils import generate_short_id
from services.db import init_db, close_connection
from services.urls import get_analytics, save_url, get_long_url

app = Flask(__name__)

with app.app_context():
    init_db()
app.teardown_appcontext(close_connection)
@app.route('/', methods=['GET', 'POST'])
def index():
    short_url = None
    if request.method == 'POST':
        long_url = request.form.get('url')
        if long_url:
            short_id = generate_short_id()
            save_url(short_id, long_url)
            short_url = request.host_url + 's/' + short_id
    return render_template('index.html', short_url=short_url)


@app.route('/shorten', methods=['POST'])
def shorten():
    data = request.get_json()
    long_url = data.get('url')
    if not long_url:
        return jsonify({'error': 'Missing URL'}), 400
    short_id = generate_short_id()
    save_url(short_id, long_url)
    short_url = request.host_url + 's/' + short_id
    return jsonify({'short_url': short_url})


@app.route('/s/<short_id>', methods=['GET'])
def redirect_short_url(short_id):
    long_url = get_long_url(short_id)
    if long_url:
        return redirect(long_url)
    return jsonify({'error': 'URL not found'}), 404


@app.route('/analytics', methods=['GET', 'POST'])
def analytics():
    short_id = None
    long_url = None
    if request.method == 'POST':
        # Support both form and JSON
        if request.is_json:
            data = request.get_json()
            short_url = data.get('short_url')
            if not short_url:
                return jsonify({'error': 'Missing short_url'}), 400
            short_id = short_url.rstrip('/').split('/')[-1]
        else:
            short_id = request.form.get('short_id')
        if short_id:
            urls = get_analytics(short_id)
            if urls:
                long_url = urls[1]
            else:
                long_url = None
    return render_template('analytics.html', short_id=short_id, long_url=long_url)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
