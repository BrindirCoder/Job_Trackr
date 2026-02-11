def test_register_and_login(client):
    # Register
    res = client.post("/register", json={
        "username": "testuser",
        "email": "test@test.com",
        "password": "123456"
    })

    assert res.status_code == 201

    # Login
    res = client.post("/login", json={
        "email": "test@test.com",
        "password": "123456"
    })

    assert res.status_code == 200
