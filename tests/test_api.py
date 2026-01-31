"""
Simple test script for the Synova AI API.
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_root():
    """Test the root endpoint."""
    response = requests.get(f"{BASE_URL}/")
    print(f"Root endpoint: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_list_messages():
    """Test listing messages."""
    response = requests.get(f"{BASE_URL}/api/v1/messages/")
    print(f"List messages: {response.status_code}")
    print(f"Messages: {response.json()}\n")

def test_create_message():
    """Test creating a message."""
    data = {
        "tier": "terrestrial",
        "query": "Hello, Synova AI! This is a test message."
    }
    response = requests.post(
        f"{BASE_URL}/api/v1/messages/",
        json=data
    )
    print(f"Create message: {response.status_code}")
    print(f"Created message: {json.dumps(response.json(), indent=2)}\n")
    return response.json()["id"]

def test_get_message(message_id):
    """Test getting a specific message."""
    response = requests.get(f"{BASE_URL}/api/v1/messages/{message_id}")
    print(f"Get message {message_id}: {response.status_code}")
    print(f"Message: {json.dumps(response.json(), indent=2)}\n")

if __name__ == "__main__":
    print("=== Testing Synova AI API ===\n")

    try:
        test_root()
        test_list_messages()
        message_id = test_create_message()
        test_get_message(message_id)
        test_list_messages()

        print("=== All tests passed! ===")
    except Exception as e:
        print(f"Error: {e}")
