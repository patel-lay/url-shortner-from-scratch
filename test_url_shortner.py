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

