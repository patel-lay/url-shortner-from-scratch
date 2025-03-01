from flask import Flask, request, jsonify
import json 
import pytest
from app import app, set_short_url,get_url
# app.app_context().push()


# Create a fixture for test client
@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client

@pytest.fixture
def client():
    # app = create_app()
    return app.test_client()


def test_set_short_url():

    client = app.test_client()

    url = "https://codingchallenges.fyi/challenges/challenge-url-shortener"
    headers = {
        "Content-Type":'application/json'
    }
    json_test = {
        "long_url":url
    }
    response = client.post("/api", headers = headers, data = json.dumps(json_test))
    assert response.status_code == 200
    resp = json.loads(response.data)
 
    short_url = resp["short_url"]
    json_test_get = {
        "short_url": short_url
    }
 
    response = client.get("/api", headers = headers, data = json.dumps(json_test_get))
    assert response.status_code == 302
    long_url_resp = json.loads(response.data)
    assert url == long_url_resp['long_url']

def test_set_duplicate_short_url():

    client = app.test_client()

    url = "https://code.visualstudio.com/docs/languages/markdown"
    headers = {
        "Content-Type":'application/json'
    }
    json_test = {
        "long_url":url
    }
    response = client.post("/api", headers = headers, data = json.dumps(json_test))
    assert response.status_code == 200
    resp = json.loads(response.data)

    short_url = resp["short_url"]


    #send duplicate request, no changes should be expected in response
    response2 = client.post("/api", headers = headers, data = json.dumps(json_test))
    assert response2.status_code == 200

    resp2 = json.loads(response2.data)
    short_url2 = resp2["short_url"]

    assert short_url == short_url2




# def test_add_url():
#     client = app.test_client()
#     url = "/add"
#     json_test = {
#         "url":"https://gmail.com"
#     }
#     url_testing = {
#         "url":"https://whatishappening.com"
#     }
#     headers = {
#         "Content-Type":'application/json'
#     }
#     res = client.post(url, headers= headers, data = json.dumps(json_test))
#     assert res.status_code == 302
#     res = client.post(url, headers= headers, data = json.dumps(url_testing))
#     assert b"url already exsists" in res.get_data()

# def test_add_mock(requests_mock):
#     url = "https://127.0.0.1/add"
#     headers = {
#         "Content-Type":'application/json'
#     }
#     expected_text = "url already exsists"
#     requests_mock.post(url,status_code=302,text = json.dumps(expected_text),headers=headers )
#     response = requests.post("https://127.0.0.1/add", headers=headers, json=({"url":"https://espn.com"}))
#     assert response.status_code == 302
#     assert "url already exsists" in response.json()
#     new_text = "Succesfully added to DB"
#     requests_mock.post(url,status_code=302,text = json.dumps(new_text),headers=headers )
#     response = requests.post("https://127.0.0.1/add", headers=headers, json=({"url":"https://gmail.com"}))
#     assert "Succesfully added to DB" in response.json()

# def test_url_key():
#     json_test = {
#         "dhu":"https://gmail.com"
#     }
#     test = False
#     if 'url' in json_test.keys():
#         assert test == False


# def test_query_db():
#     test_url = Url("KtM5543","https://localhost/KtM5543","https://gmail.com")
#     db.session.add(test_url)
#     url_db = Url.query.filter(Url.long_url == "https://gmail.com").first()
#     assert url_db.key == "KtM5543"
#     assert url_db.short_url == "https://localhost/KtM5543"
#     assert url_db.long_url == "https://gmail.com"

#     url_db = Url.query.filter(Url.long_url == "https://shouldbenone.com").first()
#     assert url_db == None

# def test_url_redirect():
#     client = app.test_client()
#     url = "/redirect/KtM5543"
#     res = client.get(url)
#     assert res.status_code == 302
#     url = "/redirect/hello"
#     res = client.get(url)
#     assert b"This short url does not exist" in res.get_data()
#     post_req = client.post(url)
#     assert post_req.status_code == 405