from api_test.schemas.users import login


def test_login_valid_credentials(client, assertions, config, users_data):
    method = "POST"
    url = f"{config.base_url}/users/login"
    json = users_data.get_payload_to_login(email=config.logged_in_email, password=config.logged_in_email_password)

    response = client.send_request(method=method, url=url, json=json)

    assertions.validate_status_code(response=response, expected_status_code=200)
    assertions.validate_json_schema_pydantic(json=response.json(), model=login.SchemaLoginSuccess)