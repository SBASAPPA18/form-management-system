from fastapi import status

def test_create_form(client, db):
    # Register and login
    register_response = client.post(
        "/auth/register",
        json={
            "username": "formuser",
            "email": "form@example.com",
            "password": "strongpassword123"
        }
    )
    
    login_response = client.post(
        "/auth/login",
        data={
            "username": "form@example.com",
            "password": "strongpassword123"
        }
    )
    access_token = login_response.json()["access_token"]
    
    # Create a form
    response = client.post(
        "/forms/create",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "title": "Test Form",
            "description": "A test form for pytest",
            "fields": [
                {
                    "field_id": "name",
                    "type": "string",
                    "label": "Name",
                    "required": True
                }
            ]
        }
    )
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "Test Form"