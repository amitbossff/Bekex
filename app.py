from flask import Flask, render_template, request, jsonify
from google_play_scraper import reviews, Sort
import re

app = Flask(__name__)

def extract_package_name(url):
    match = re.search(r'id=([a-zA-Z0-9._]+)', url)
    return match.group(1) if match else None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch', methods=['POST'])
def fetch_reviews():
    data = request.json
    link = data.get('link')
    cursor = data.get('cursor')

    package_name = extract_package_name(link)
    if not package_name:
        return jsonify({"error": "Invalid link"})

    result, next_cursor = reviews(
        package_name,
        lang='en',
        country='in',
        sort=Sort.NEWEST,
        count=200,
        continuation_token=cursor
    )

    grouped = {}
    for r in result:
        date = r['at'].date().isoformat()
        grouped.setdefault(date, []).append(r['userName'])

    return jsonify({
        "data": grouped,
        "cursor": next_cursor
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
