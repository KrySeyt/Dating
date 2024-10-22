def test_get_me(client):
    input_data = {
        "username": "testusername",
        "password": "123456qwerty"
    }

    client.post("/users", json=input_data)
    client.post("/users/login", json=input_data)

    expected_result = {
        "id": 1,
        "username": "testusername",
    }

    response = client.get(f"/users/me")
    assert response.json() == expected_result
    assert response.status_code == 200


def test_get_user(client):
    input_data = {
        "username": "testusername",
        "password": "123456qwerty"
    }

    user_id = client.post("/users", json=input_data).json()["id"]

    expected_result = {
        "id": 1,
        "username": "testusername",
    }

    response = client.get(f"/users/{user_id}")
    assert response.json() == expected_result
    assert response.status_code == 200


def test_login(client):
    input_data = {
        "username": "testusername",
        "password": "123456qwerty"
    }

    client.post("/users", json=input_data)

    response = client.post(f"/users/login", json=input_data)

    assert "Authorization" in response.cookies
    assert response.status_code == 200


def test_logout(client):
    input_data = {
        "username": "testusername",
        "password": "123456qwerty"
    }

    client.post("/users", json=input_data)
    client.post(f"/users/login", json=input_data)

    response = client.post(f"/users/logout", json=input_data)

    assert "Authorization" not in response.cookies
    assert response.status_code == 200


def test_register(client):
    input_data = {
        "username": "testusername",
        "password": "123456qwerty"
    }

    expected_result = {
        "id": 1,
        "username": "testusername",
    }

    response = client.post("/users", json=input_data)

    assert response.json() == expected_result
    assert response.status_code == 201
