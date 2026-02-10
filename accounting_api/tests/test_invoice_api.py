from fastapi.testclient import TestClient


def test_invoice_flow(
        client: TestClient,
        auth_headers: dict[str, str]
        ) -> None:
    # Create customer
    res = client.post(
        "/customers/",
        headers=auth_headers,
        json={"name": "Ali", "email": "ali@gmail.com"}
    )
    customer_id = res.json()["id"]

    # Create invoice
    res = client.post(
        "/invoices/",
        headers=auth_headers,
        json={"customer_id": customer_id})
    assert res.status_code == 201
    invoice_id = res.json()["id"]

    # Add items
    client.post(
        f"/invoices/{invoice_id}/items",
        json={"description": "A", "quantity": 2, "unit_price": 10},
    )
    client.post(
        f"/invoices/{invoice_id}/items",
        json={"description": "B", "quantity": 1, "unit_price": 5},
    )

    # Fetch
    res = client.get(f"/invoices/{invoice_id}")
    data = res.json()

    assert data["total_amount"] == 25
    assert len(data["line_items"]) == 2
