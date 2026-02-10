from fastapi.testclient import TestClient


def test_create_and_get_customer(
        client: TestClient,
        auth_headers: dict[str, str]
        ) -> None:
    # Create a new customer
    response = client.post(
        "/customers/",
        headers=auth_headers,
        json={"name": "Ardo0", "email": "it.arghavanemami@gmail.com"}
    )
    assert response.status_code == 201
    created_customer = response.json()
    assert created_customer["name"] == "Ardo0"
    assert created_customer["email"] == "it.arghavanemami@gmail.com"
    customer_id = created_customer["id"]

    # List
    response = client.get("/customers/")
    assert response.status_code == 200
    assert len(response.json()) >= 1

    # Get by ID
    response = client.get(f"/customers/{customer_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Ardo0"

    # Delete
    response = client.delete(f"/customers/{customer_id}")
    assert response.status_code == 204

    # Verify Deletion
    response = client.get(f"/customers/{customer_id}")
    assert response.status_code == 404
