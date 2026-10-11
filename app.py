"""ReleaseLab sample service.

Built for practising CI/CD, canary deploys and probe-based traffic shifting:
- /health  -> liveness probe (always UP while the process runs)
- /ready   -> readiness probe (503 until the startup delay elapses)
- /version -> reports the configured APP_VERSION
"""

import os
import time
from typing import Any

from flask import Flask, jsonify

_TRUTHY = {"1", "true", "yes", "on"}


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in _TRUTHY


def create_app(config: dict[str, Any] | None = None) -> Flask:
    """Application factory.

    Config resolution order (later wins):
      1. Environment variables: APP_VERSION, READY_DELAY_SECONDS, NEVER_READY
      2. The optional `config` mapping (used by tests / embedders).
    """
    app = Flask(__name__)

    # Defaults from the environment.
    app.config["APP_VERSION"] = os.getenv("APP_VERSION", "v1")
    app.config["READY_DELAY_SECONDS"] = int(os.getenv("READY_DELAY_SECONDS", "0"))
    app.config["NEVER_READY"] = _as_bool(os.getenv("NEVER_READY", "false"))
    app.config["STARTED_AT"] = time.monotonic()

    # Caller-supplied overrides (this is what the tests inject).
    if config:
        app.config.update({k: v for k, v in config.items() if k.isupper()})

    @app.get("/")
    def home():
        return jsonify(service="ReleaseLab", version=app.config["APP_VERSION"])

    @app.get("/health")
    def health():
        return jsonify(status="UP", version=app.config["APP_VERSION"]), 200

    @app.get("/ready")
    def ready():
        never_ready = _as_bool(app.config.get("NEVER_READY", False))
        delay = int(app.config.get("READY_DELAY_SECONDS", 0))
        elapsed = time.monotonic() - app.config["STARTED_AT"]

        if never_ready or elapsed < delay:
            return jsonify(status="NOT_READY"), 503
        return jsonify(status="READY"), 200

    @app.get("/version")
    def get_version():
        return jsonify(version=app.config["APP_VERSION"]), 200

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
