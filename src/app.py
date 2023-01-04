import os
import json
import pandas as pd

from flask import Flask, request
from autoviz.AutoViz_Class import AutoViz_Class
from pymongo import MongoClient
from minio import Minio
from io import BytesIO

FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))
FLASK_DEBUG = bool(os.getenv("FLASK_DEBUG", True))
MONGO_HOST = os.getenv("MONGO_HOST", "0.0.0.0")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MINIO_HOST = os.getenv("MINIO_HOST", "0.0.0.0")
MINIO_PORT = int(os.getenv("MINIO_PORT", 9000))
MINIO_USER = os.getenv("MINIO_USER", "minioadmin")
MINIO_PASS = os.getenv("MINIO_PASS", "minioadmin")

app = Flask(__name__)
db = MongoClient(MONGO_HOST, MONGO_PORT)
s3 = Minio(f"{MINIO_HOST}:{MINIO_PORT}", MINIO_USER, MINIO_PASS, secure=False)
av = AutoViz_Class()

# TODO: Temp thing, remove later
images = dict()


@app.route("/", methods=["POST"])
def index():
    data = json.loads(request.data)

    if not ("minio-input" in data):
        return "Missing fields in request data", 400

    bucket, file = data["minio-input"].split("/", 1)
    response = s3.get_object(bucket, file)
    buffer = BytesIO(response.read())
    buffer.seek(0)
    df = pd.read_csv(buffer)

    chart = av.AutoViz(
        filename="",
        dfte=df,
    )

    print(chart)

    return "ok"


@app.errorhandler(Exception)
def exception_handler(ex: Exception):
    return str(ex), 500


if __name__ == "__main__":
    app.run(FLASK_HOST, FLASK_PORT, FLASK_DEBUG)
