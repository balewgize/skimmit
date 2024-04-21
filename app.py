import logging
from flask import Flask, request, jsonify, make_response, render_template

from .utils.downloader import get_article_text, get_youtube_transcript
from .summary import summarize_text

app = Flask(__name__)


logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/summarize", methods=["GET", "POST"])
def skimmit():
    if request.method == "GET":
        return render_template("index.html")

    elif request.method == "POST":
        data = request.get_json()

        url = data.get("url")
        source_type = data.get("source")

        if source_type == "article":
            source_text = get_article_text(url)
        elif source_type == "video":
            source_text = get_youtube_transcript(url)
        else:
            return make_response(jsonify({"error": "Invalid source type"}), 400)

        summary = summarize_text(source_text, source_type)
        return jsonify(summary), 200


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({"error": "Bad request"}), 400)


if __name__ == "__main__":
    app.run(debug=False)
