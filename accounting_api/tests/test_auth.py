from fastapi.testclient import TestClient


def test_missing_api_key(client: TestClient):
    response = client.post(
        "/customers/",
        json={"name": "NoKey", "email": "Nokey@gmail.com"}
    )
    assert response.status_code == 422  # Missing header results in 422


def test_invalid_api_key(client: TestClient):
    response = client.post(
        "/customers/",
        headers={"X-API-KEY": "invalid_key"},
        json={"name": "InvalidKey", "email": "InvalidKey@gmail.com"}
    )
    assert response.status_code == 401  # Unauthorized due to invalid API key


def test_create_and_get_customer_with_api_key(
        client: TestClient,
        auth_headers: dict[str, str]
        ):
    response = client.post(
        "/customers/",
        headers=auth_headers,
        json={"name": "ValidKey", "email": "validKey@gmail.com"}
    )
    assert response.status_code == 201
