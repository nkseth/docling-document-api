import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to FastAPI Server!", "docs": "/docs"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "fastapi-server"}

def test_create_item():
    item_data = {
        "name": "Test Item",
        "description": "A test item",
        "price": 99.99,
        "tax": 9.99
    }
    response = client.post("/items", json=item_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == item_data["name"]
    assert data["price"] == item_data["price"]
    assert data["id"] is not None

def test_get_items():
    # First create an item
    item_data = {
        "name": "Test Item 2",
        "description": "Another test item",
        "price": 149.99
    }
    client.post("/items", json=item_data)
    
    # Then get all items
    response = client.get("/items")
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)
    assert len(items) > 0

def test_get_item():
    # Create an item first
    item_data = {
        "name": "Specific Test Item",
        "price": 299.99
    }
    create_response = client.post("/items", json=item_data)
    created_item = create_response.json()
    item_id = created_item["id"]
    
    # Get the specific item
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["name"] == item_data["name"]

def test_get_nonexistent_item():
    response = client.get("/items/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

def test_update_item():
    # Create an item first
    item_data = {
        "name": "Item to Update",
        "price": 199.99
    }
    create_response = client.post("/items", json=item_data)
    created_item = create_response.json()
    item_id = created_item["id"]
    
    # Update the item
    update_data = {
        "name": "Updated Item",
        "price": 249.99
    }
    response = client.put(f"/items/{item_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["price"] == update_data["price"]

def test_delete_item():
    # Create an item first
    item_data = {
        "name": "Item to Delete",
        "price": 99.99
    }
    create_response = client.post("/items", json=item_data)
    created_item = create_response.json()
    item_id = created_item["id"]
    
    # Delete the item
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 200
    assert "deleted successfully" in response.json()["message"]
    
    # Verify it's deleted
    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 404