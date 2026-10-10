import time
from app import create_app


def make_client(**config):
    app = create_app(config)
    app.config["TESTING"] = True
    return app, app.test_client()


def test_health_is_up():
    _, client = make_client(APP_VERSION="v1", READY_DELAY_SECONDS=0, NEVER_READY=False)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "UP"


def test_version_comes_from_configuration():
    _, client = make_client(APP_VERSION="v2", READY_DELAY_SECONDS=0, NEVER_READY=False)
    response = client.get("/version")
    assert response.status_code == 200
    assert response.get_json()["version"] == "v2"


def test_ready_when_no_delay():
    _, client = make_client(APP_VERSION="v1", READY_DELAY_SECONDS=0, NEVER_READY=False)
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.get_json()["status"] == "READY"


def test_never_ready_returns_503():
    _, client = make_client(APP_VERSION="v3", READY_DELAY_SECONDS=0, NEVER_READY=True)
    response = client.get("/ready")
    assert response.status_code == 503
    assert response.get_json()["status"] == "NOT_READY"


def test_delayed_readiness_returns_503_then_200():
    app, client = make_client(
        APP_VERSION="v2",
        READY_DELAY_SECONDS=10,
        NEVER_READY=False,
    )

    first_response = client.get("/ready")
    assert first_response.status_code == 503

    # Simulate that the configured startup delay has elapsed.
    app.config["STARTED_AT"] = time.monotonic() - 11
    second_response = client.get("/ready")
    assert second_response.status_code == 200
    assert second_response.get_json()["status"] == "READY"
