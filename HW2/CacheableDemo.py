import datetime
from flask import Flask, jsonify
from flask_caching import Cache

app = Flask(__name__)

cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})


@app.route("/time")
@cache.cached(timeout=60)
def get_time():
    print("Server ĐANG tính toán lại thời gian cho /time...")

    data = {
        "time": str(datetime.datetime.now())
    }
    return jsonify(data)


@app.route("/data")
@cache.cached(timeout=30)
def data():
    print("Server ĐANG xử lý request cho /data...")

    return jsonify({"message": "Hello API"})


if __name__ == "__main__":
    app.run(debug=True)