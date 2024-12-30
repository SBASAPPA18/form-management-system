from fastapi import status

def test_register_user(client):
    # Test user registration
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "strongpassword123"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert "id" in response.json()
    assert response.json()["email"] == "test@example.com"

def test_login_user(client, db):
    # First, register a user
    client.post(
        "/auth/register",
        json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "strongpassword123"
        }
    )
    
    # Then try to login
    response = client.post(
        "/auth/login",
        data={
            "username": "login@example.com",
            "password": "strongpassword123"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()