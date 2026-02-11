def login(client):
    client.post("/register", json={
        "username": "user1",
        "email": "user1@test.com",
        "password": "123456"
    })

    res = client.post("/login", json={
        "email": "user1@test.com",
        "password": "123456"
    })

    token = res.json["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_application(client):
    headers = login(client)

    res = client.post(
        "/applications",
        headers=headers,
        json={
            "company_name": "OpenAI",
            "position_title": "Backend Engineer",
            "location": "Remote",
            "status": "Applied"
        }
    )

    print(res.status_code, res.json)   

    assert res.status_code == 201



def test_list_applications(client):
    headers = login(client)

    client.post("/applications",
        headers=headers,
        json={
            "company_name": "Google",
            "position_title": "Backend Dev"
        }
    )

    res = client.get("/applications", headers=headers)

    assert res.status_code == 200
    assert len(res.json) == 1
