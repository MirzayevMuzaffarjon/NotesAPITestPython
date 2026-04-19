import pytest_check as check

def test_health_check_returns_200(client, config, assertions):
    method = "GET"
    url = f"{config.base_url}/health-check"

    response = client.send_request(method=method, url=url)
    assertions.validate_status_code(response=response, expected_status_code=200)


def test_health_check_response_body(client, config, assertions):
    method = "GET"
    url = f"{config.base_url}/health-check"

    response = client.send_request(method=method, url=url)
    check.equal(response.json()["success"], True)
    check.equal(response.json()["status"], 200)
    check.equal(response.json()["message"], "Notes API is Running")