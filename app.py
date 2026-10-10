import os
import time
from flask import Flask, jsonify


def env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.update(
        APP_VERSION=os.getenv("APP_VERSION", "v1"),
        READY_DELAY_SECONDS=float(os.getenv("READY_DELAY_SECONDS", "0")),
        NEVER_READY=env_bool("NEVER_READY", False),
    )

    if test_config:
        app.config.update(test_config)

    # Monotonic clock is suitable for measuring elapsed time.
    app.config["STARTED_AT"] = time.monotonic()

    @app.get("/")
    def index():
        return jsonify(
            application="ReleaseLab",
            version=app.config["APP_VERSION"],
            endpoints=["/health", "/ready", "/version"],
        )

    @app.get("/health")
    def health():
        # Liveness: process is running. Readiness is checked separately.
        return jsonify(status="UP", version=app.config["APP_VERSION"]), 200

    @app.get("/ready")
    def ready():
        if app.config["NEVER_READY"]:
            return jsonify(status="NOT_READY", reason="NEVER_READY enabled"), 503

        elapsed = time.monotonic() - app.config["STARTED_AT"]
        delay = max(0.0, float(app.config["READY_DELAY_SECONDS"]))

        if elapsed < delay:
            return jsonify(
                status="NOT_READY",
                reason="startup delay",
                retry_after_seconds=round(delay - elapsed, 2),
            ), 503

        return jsonify(status="READY", version=app.config["APP_VERSION"]), 200

    @app.get("/version")
    def version():
        return jsonify(application="ReleaseLab", version=app.config["APP_VERSION"]), 200

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
