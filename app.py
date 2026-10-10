
import os
import time
from flask import Flask, jsonify


def create_app():
    app = Flask(__name__)

    version = os.getenv("APP_VERSION", "v1")
    delay = int(os.getenv("READY_DELAY_SECONDS", "0"))
    never_ready = os.getenv("NEVER_READY", "false").lower() == "true"
    started = time.time()

    @app.get("/")
    def home():
        return jsonify(service="ReleaseLab", version=version)

    @app.get("/health")
    def health():
        return jsonify(status="healthy", version=version), 200

    @app.get("/ready")
    def ready():
        if never_ready or time.time() - started < delay:
            return jsonify(status="not_ready"), 503
        return jsonify(status="ready"), 200

    @app.get("/version")
    def get_version():
        return jsonify(version=version), 200

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
