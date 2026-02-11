import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def log(message):
    print(f"[TEST] {message}")

def test_endpoints():
    log("Starting API tests...")

    # Wait for server to be ready
    try:
        requests.get(f"{BASE_URL}/")
    except requests.exceptions.ConnectionError:
        log("Server not ready, waiting...")
        time.sleep(2)

    # 1. Create a user
    log("1. Creating a user...")
    user_data = {
        "username": "testuser_01",
        "email": "testuser_01@example.com"
    }
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    
    if response.status_code == 201:
        user = response.json()
        log(f"User created successfully: {user}")
        user_id = user['id']
    else:
        log(f"Failed to create user: {response.status_code} - {response.text}")
        # If user already exists (testing multiple runs), let's try to fetch it or continue
        if "already exists" in response.text:
             log("User might already exist, trying to fetch all users to find ID...")
        return

    # 2. Read all users
    log("\n2. Reading all users...")
    response = requests.get(f"{BASE_URL}/users/")
    if response.status_code == 200:
        users = response.json()
        log(f"Users found: {len(users)}")
        # Verify our user is in the list
        found = any(u['id'] == user_id for u in users)
        log(f"Created user found in list: {found}")
    else:
        log(f"Failed to read users: {response.status_code}")

    # 3. Read specific user
    log(f"\n3. Reading user with ID {user_id}...")
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    if response.status_code == 200:
        log(f"User details: {response.json()}")
    else:
        log(f"Failed to read user: {response.status_code}")

    # 4. Update user
    log(f"\n4. Updating user with ID {user_id}...")
    update_data = {
        "username": "testuser_01_updated",
        "email": "updated_01@example.com"
    }
    response = requests.put(f"{BASE_URL}/users/{user_id}", json=update_data)
    if response.status_code == 200:
        log(f"User updated successfully: {response.json()}")
    else:
        log(f"Failed to update user: {response.status_code}")

    # 5. Delete user
    log(f"\n5. Deleting user with ID {user_id}...")
    response = requests.delete(f"{BASE_URL}/users/{user_id}")
    if response.status_code == 204:
        log("User deleted successfully")
    else:
        log(f"Failed to delete user: {response.status_code}")

    # Verify deletion
    log("\nTarget check: verifying deletion...")
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    if response.status_code == 404:
        log("Verification successful: User not found")
    else:
        log(f"Verification failed: User still exists or other error: {response.status_code}")

if __name__ == "__main__":
    test_endpoints()
