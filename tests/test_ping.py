import pytest


"""
Simple test for our "ping" endpoint
"""

def test_successful_ping(client, app):
    response = client.get('/ping')

    assert response.status_code == 200
    response_body = response.json
    assert response_body["message"] == "pong!"
