from flask import Flask, request, jsonify, send_file
from google_play_scraper import reviews, Sort
from datetime import datetime, date

app = Flask(__name__)

@app.route("/")
def home():
    return send_file("index.html")


@app.route("/reviews")
def get_reviews():
    link = request.args.get("link")
    date_str = request.args.get("date")
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 200))  # default 200

    if not link or not date_str:
        return jsonify({"status": "error", "data": []})

    target_date = datetime.strptime(date_str, "%Y-%m-%d").date()

    if "id=" in link:
        app_id = link.split("id=")[1].split("&")[0]
    else:
        app_id = link

    result, _ = reviews(
        app_id,
        lang="en",
        country="in",
        sort=Sort.NEWEST,
        count=15000
    )

    day_reviews = []
    seen = set()

    for r in result:
        if r.get("at") and r["at"].date() == target_date:
            name = r["userName"]
            if name not in seen:
                seen.add(name)
                day_reviews.append({"user": name})

    total = len(day_reviews)
    sliced = day_reviews[offset: offset + limit]

    return jsonify({
        "status": "success",
        "total": total,
        "returned": len(sliced),
        "data": sliced
    })


if __name__ == "__main__":
    app.run(debug=True)
