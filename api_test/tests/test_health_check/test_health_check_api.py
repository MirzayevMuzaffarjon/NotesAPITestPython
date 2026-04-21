import pytest_check as check
from api_test.schemas.health_check import SchemaHealthCheck


def test_health_check_returns_200(client, assertions):
    """Verify health check endpoint returns 200 status code."""
    response = client.send_request(method="GET", endpoint="/health-check")
    assertions.validate_status_code(response=response, expected_status_code=200)
    assertions.validate_json_schema_pydantic(
        json_data=response.json(), 
        model=SchemaHealthCheck
    )


def test_health_check_response_body(client, assertions):
    """Verify health check response body contains expected values."""
    response = client.send_request(method="GET", endpoint="/health-check")
    json_data = response.json()
    
    check.equal(json_data["success"], True)
    check.equal(json_data["status"], 200)
    check.equal(json_data["message"], "Notes API is Running")
