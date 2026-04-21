"""Tests for user login endpoint."""
from api_test.schemas.users import SchemaLoginSuccess, SchemaLoginErrorCase


def test_login_valid_credentials(client, assertions, config):
    """Test login with valid credentials."""
    json_data = {
        "email": config.logged_in_email,
        "password": config.logged_in_password
    }

    response = client.send_request(method="POST", endpoint="/users/login", json=json_data)

    assertions.validate_status_code(response=response, expected_status_code=200)
    assertions.validate_json_schema_pydantic(
        json_data=response.json(), 
        model=SchemaLoginSuccess
    )


def test_login_validate_if_data_is_right(client, assertions, config):
    """Test that login returns correct user data."""
    json_data = {
        "email": config.logged_in_email,
        "password": config.logged_in_password
    }

    response = client.send_request(method="POST", endpoint="/users/login", json=json_data)
    response_data = response.json()

    assertions.validate_status_code(response=response, expected_status_code=200)
    assertions.validate_to_equality(a=response_data["data"]["id"], b="68f6937fd5b6520297774e3a")
    assertions.validate_to_equality(a=response_data["data"]["name"], b="MuzaffarjonMirzayev")
    assertions.validate_to_equality(a=response_data["data"]["email"], b="mirzayevmuzaffar525@gmail.com")


def test_login_with_incorrect_password(client, assertions, config):
    """Test login with incorrect password returns 401."""
    json_data = {
        "email": config.logged_in_email,
        "password": "InValidPassword"
    }

    response = client.send_request(method="POST", endpoint="/users/login", json=json_data)

    assertions.validate_status_code(response=response, expected_status_code=401)
    assertions.validate_json_schema_pydantic(
        json_data=response.json(), 
        model=SchemaLoginErrorCase
    )


def test_login_with_un_auth_email_and_password(client, assertions):
    """Test login with unauthorized email and password returns 401."""
    json_data = {
        "email": "tttlllkkk144@grh.kl",
        "password": "InValidPassword"
    }

    response = client.send_request(method="POST", endpoint="/users/login", json=json_data)

    assertions.validate_status_code(response=response, expected_status_code=401)
    assertions.validate_json_schema_pydantic(
        json_data=response.json(), 
        model=SchemaLoginErrorCase
    )


def test_login_with_empty_password(client, assertions, config):
    """Test login with empty password returns 400."""
    json_data = {
        "email": config.logged_in_email,
        "password": ""
    }

    response = client.send_request(method="POST", endpoint="/users/login", json=json_data)

    assertions.validate_status_code(response=response, expected_status_code=400)
    assertions.validate_json_schema_pydantic(
        json_data=response.json(), 
        model=SchemaLoginErrorCase
    )


def test_login_with_empty_email_and_password(client, assertions, config):
    """Test login with empty email and password returns 400."""
    json_data = {
        "email": "",
        "password": ""
    }

    response = client.send_request(method="POST", endpoint="/users/login", json=json_data)

    assertions.validate_status_code(response=response, expected_status_code=400)
    assertions.validate_json_schema_pydantic(
        json_data=response.json(), 
        model=SchemaLoginErrorCase
    )


def test_login_with_empty_payload(client, assertions, config):
    """Test login with empty payload returns 400."""
    response = client.send_request(method="POST", endpoint="/users/login", json={})

    assertions.validate_status_code(response=response, expected_status_code=400)
    assertions.validate_json_schema_pydantic(
        json_data=response.json(), 
        model=SchemaLoginErrorCase
    )


def test_login_with_invalid_email_format(client, assertions, config):
    """Test login with invalid email format returns 400."""
    json_data = {
        "email": "invalid-email-format",
        "password": config.logged_in_password
    }

    response = client.send_request(method="POST", endpoint="/users/login", json=json_data)

    assertions.validate_status_code(response=response, expected_status_code=400)
    assertions.validate_json_schema_pydantic(
        json_data=response.json(), 
        model=SchemaLoginErrorCase
    )


def test_login_with_sql_injection_in_email(client, assertions, config):
    """Test login with SQL injection attempt in email returns 400."""
    json_data = {
        "email": "admin' OR '1'='1",
        "password": "anypassword"
    }

    response = client.send_request(method="POST", endpoint="/users/login", json=json_data)

    assertions.validate_status_code(response=response, expected_status_code=400)
    assertions.validate_json_schema_pydantic(
        json_data=response.json(), 
        model=SchemaLoginErrorCase
    )


def test_login_with_sql_injection_in_password(client, assertions, config):
    """Test login with SQL injection attempt in password returns 401."""
    json_data = {
        "email": config.logged_in_email,
        "password": "' OR '1'='1"
    }

    response = client.send_request(method="POST", endpoint="/users/login", json=json_data)

    assertions.validate_status_code(response=response, expected_status_code=401)
    assertions.validate_json_schema_pydantic(
        json_data=response.json(), 
        model=SchemaLoginErrorCase
    )


def test_login_with_very_long_email(client, assertions, config):
    """Test login with very long email returns 400."""
    long_email = "a" * 500 + "@example.com"
    json_data = {
        "email": long_email,
        "password": "anypassword"
    }

    response = client.send_request(method="POST", endpoint="/users/login", json=json_data)

    assertions.validate_status_code(response=response, expected_status_code=400)
    assertions.validate_json_schema_pydantic(
        json_data=response.json(), 
        model=SchemaLoginErrorCase
    )


def test_login_with_very_long_password(client, assertions, config):
    """Test login with very long password returns 400."""
    long_password = "p" * 1000
    json_data = {
        "email": config.logged_in_email,
        "password": long_password
    }

    response = client.send_request(method="POST", endpoint="/users/login", json=json_data)

    assertions.validate_status_code(response=response, expected_status_code=400)
    assertions.validate_json_schema_pydantic(
        json_data=response.json(), 
        model=SchemaLoginErrorCase
    )


def test_login_with_whitespace_only_email(client, assertions, config):
    """Test login with whitespace only email returns 400."""
    json_data = {
        "email": "   ",
        "password": config.logged_in_password
    }

    response = client.send_request(method="POST", endpoint="/users/login", json=json_data)

    assertions.validate_status_code(response=response, expected_status_code=400)
    assertions.validate_json_schema_pydantic(
        json_data=response.json(), 
        model=SchemaLoginErrorCase
    )


def test_login_with_whitespace_only_password(client, assertions, config):
    """Test login with whitespace only password returns 400."""
    json_data = {
        "email": config.logged_in_email,
        "password": "   "
    }

    response = client.send_request(method="POST", endpoint="/users/login", json=json_data)

    assertions.validate_status_code(response=response, expected_status_code=400)
    assertions.validate_json_schema_pydantic(
        json_data=response.json(), 
        model=SchemaLoginErrorCase
    )


def test_login_with_missing_email_field(client, assertions, config):
    """Test login with missing email field returns 400."""
    json_data = {"password": config.logged_in_password}

    response = client.send_request(method="POST", endpoint="/users/login", json=json_data)

    assertions.validate_status_code(response=response, expected_status_code=400)
    assertions.validate_json_schema_pydantic(
        json_data=response.json(), 
        model=SchemaLoginErrorCase
    )


def test_login_with_missing_password_field(client, assertions, config):
    """Test login with missing password field returns 400."""
    json_data = {"email": config.logged_in_email}

    response = client.send_request(method="POST", endpoint="/users/login", json=json_data)

    assertions.validate_status_code(response=response, expected_status_code=400)
    assertions.validate_json_schema_pydantic(
        json_data=response.json(), 
        model=SchemaLoginErrorCase
    )


def test_login_with_null_values(client, assertions, config):
    """Test login with null values returns 400."""
    json_data = {"email": None, "password": None}

    response = client.send_request(method="POST", endpoint="/users/login", json=json_data)

    assertions.validate_status_code(response=response, expected_status_code=400)
    assertions.validate_json_schema_pydantic(
        json_data=response.json(), 
        model=SchemaLoginErrorCase
    )


def test_login_with_special_characters_in_password(client, assertions, config):
    """Test login with special characters in password returns 400."""
    special_password = "P@$$w0rd!#$%^&*()_+-=[]{}|;':\",./<>?"
    json_data = {
        "email": config.logged_in_email,
        "password": special_password
    }

    response = client.send_request(method="POST", endpoint="/users/login", json=json_data)

    assertions.validate_status_code(response=response, expected_status_code=400)
    assertions.validate_json_schema_pydantic(
        json_data=response.json(), 
        model=SchemaLoginErrorCase
    )