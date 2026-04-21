from api_test.schemas.users import login


def test_login_valid_credentials(client, assertions, config, users_data):
    method = "POST"
    url = f"{config.base_url}/users/login"
    json = users_data.get_payload_to_login(email=config.logged_in_email, password=config.logged_in_email_password)

    response = client.send_request(method=method, url=url, json=json)

    assertions.validate_status_code(response=response, expected_status_code=200)
    assertions.validate_json_schema_pydantic(json=response.json(), model=login.SchemaLoginSuccess)


def test_login_validate_if_data_is_right(client, assertions, config, users_data):
    method = "POST"
    url = f"{config.base_url}/users/login"
    json = users_data.get_payload_to_login(email=config.logged_in_email, password=config.logged_in_email_password)

    response = client.send_request(method=method, url=url, json=json)
    json_data = response.json()

    assertions.validate_status_code(response=response, expected_status_code=200)
    assertions.validate_to_equality(a=json_data["data"]["id"], b="68f6937fd5b6520297774e3a")
    assertions.validate_to_equality(a=json_data["data"]["name"], b="MuzaffarjonMirzayev")
    assertions.validate_to_equality(a=json_data["data"]["email"], b="mirzayevmuzaffar525@gmail.com")


def test_login_with_incorrect_password(client, assertions, config, users_data):
    method = "POST"
    url = f"{config.base_url}/users/login"
    json = users_data.get_payload_to_login(email=config.logged_in_email, password="InValidPassword")

    response = client.send_request(method=method, url=url, json=json)

    assertions.validate_status_code(response=response, expected_status_code=401)
    assertions.validate_json_schema_pydantic(json=response.json(), model=login.SchemaLoginErrorCase)


def test_login_with_un_auth_email_and_password(client, assertions, config, users_data):
    method = "POST"
    url = f"{config.base_url}/users/login"
    json = users_data.get_payload_to_login(email="tttlllkkk144@grh.kl", password="InValidPassword")

    response = client.send_request(method=method, url=url, json=json)

    assertions.validate_status_code(response=response, expected_status_code=401)
    assertions.validate_json_schema_pydantic(json=response.json(), model=login.SchemaLoginErrorCase)


def test_login_with_empty_password(client, assertions, config, users_data):
    method = "POST"
    url = f"{config.base_url}/users/login"
    json = users_data.get_payload_to_login(email=config.logged_in_email, password="")

    response = client.send_request(method=method, url=url, json=json)

    assertions.validate_status_code(response=response, expected_status_code=400)
    assertions.validate_json_schema_pydantic(json=response.json(), model=login.SchemaLoginErrorCase)


def test_login_with_empty_email_and_password(client, assertions, config, users_data):
    method = "POST"
    url = f"{config.base_url}/users/login"
    json = users_data.get_payload_to_login(email="", password="")

    response = client.send_request(method=method, url=url, json=json)

    assertions.validate_status_code(response=response, expected_status_code=400)
    assertions.validate_json_schema_pydantic(json=response.json(), model=login.SchemaLoginErrorCase)


def test_login_with_empty_payload(client, assertions, config, users_data):
    method = "POST"
    url = f"{config.base_url}/users/login"
    json = {}

    response = client.send_request(method=method, url=url, json=json)

    assertions.validate_status_code(response=response, expected_status_code=400)
    assertions.validate_json_schema_pydantic(json=response.json(), model=login.SchemaLoginErrorCase)


def test_login_with_invalid_email_format(client, assertions, config, users_data):
    method = "POST"
    url = f"{config.base_url}/users/login"
    json = users_data.get_payload_to_login(email="invalid-email-format", password=config.logged_in_email_password)

    response = client.send_request(method=method, url=url, json=json)

    assertions.validate_status_code(response=response, expected_status_code=400)
    assertions.validate_json_schema_pydantic(json=response.json(), model=login.SchemaLoginErrorCase)


def test_login_with_sql_injection_in_email(client, assertions, config, users_data):
    method = "POST"
    url = f"{config.base_url}/users/login"
    json = users_data.get_payload_to_login(email="admin' OR '1'='1", password="anypassword")

    response = client.send_request(method=method, url=url, json=json)

    assertions.validate_status_code(response=response, expected_status_code=400)
    assertions.validate_json_schema_pydantic(json=response.json(), model=login.SchemaLoginErrorCase)


def test_login_with_sql_injection_in_password(client, assertions, config, users_data):
    method = "POST"
    url = f"{config.base_url}/users/login"
    json = users_data.get_payload_to_login(email=config.logged_in_email, password="' OR '1'='1")

    response = client.send_request(method=method, url=url, json=json)

    assertions.validate_status_code(response=response, expected_status_code=401)
    assertions.validate_json_schema_pydantic(json=response.json(), model=login.SchemaLoginErrorCase)


def test_login_with_very_long_email(client, assertions, config, users_data):
    method = "POST"
    url = f"{config.base_url}/users/login"
    long_email = "a" * 500 + "@example.com"
    json = users_data.get_payload_to_login(email=long_email, password="anypassword")

    response = client.send_request(method=method, url=url, json=json)

    assertions.validate_status_code(response=response, expected_status_code=400)
    assertions.validate_json_schema_pydantic(json=response.json(), model=login.SchemaLoginErrorCase)


def test_login_with_very_long_password(client, assertions, config, users_data):
    method = "POST"
    url = f"{config.base_url}/users/login"
    long_password = "p" * 1000
    json = users_data.get_payload_to_login(email=config.logged_in_email, password=long_password)

    response = client.send_request(method=method, url=url, json=json)

    assertions.validate_status_code(response=response, expected_status_code=400)
    assertions.validate_json_schema_pydantic(json=response.json(), model=login.SchemaLoginErrorCase)


def test_login_with_whitespace_only_email(client, assertions, config, users_data):
    method = "POST"
    url = f"{config.base_url}/users/login"
    json = users_data.get_payload_to_login(email="   ", password=config.logged_in_email_password)

    response = client.send_request(method=method, url=url, json=json)

    assertions.validate_status_code(response=response, expected_status_code=400)
    assertions.validate_json_schema_pydantic(json=response.json(), model=login.SchemaLoginErrorCase)


def test_login_with_whitespace_only_password(client, assertions, config, users_data):
    method = "POST"
    url = f"{config.base_url}/users/login"
    json = users_data.get_payload_to_login(email=config.logged_in_email, password="   ")

    response = client.send_request(method=method, url=url, json=json)

    assertions.validate_status_code(response=response, expected_status_code=400)
    assertions.validate_json_schema_pydantic(json=response.json(), model=login.SchemaLoginErrorCase)


def test_login_with_missing_email_field(client, assertions, config, users_data):
    method = "POST"
    url = f"{config.base_url}/users/login"
    json = {"password": config.logged_in_email_password}

    response = client.send_request(method=method, url=url, json=json)

    assertions.validate_status_code(response=response, expected_status_code=400)
    assertions.validate_json_schema_pydantic(json=response.json(), model=login.SchemaLoginErrorCase)


def test_login_with_missing_password_field(client, assertions, config, users_data):
    method = "POST"
    url = f"{config.base_url}/users/login"
    json = {"email": config.logged_in_email}

    response = client.send_request(method=method, url=url, json=json)

    assertions.validate_status_code(response=response, expected_status_code=400)
    assertions.validate_json_schema_pydantic(json=response.json(), model=login.SchemaLoginErrorCase)


def test_login_with_null_values(client, assertions, config, users_data):
    method = "POST"
    url = f"{config.base_url}/users/login"
    json = {"email": None, "password": None}

    response = client.send_request(method=method, url=url, json=json)

    assertions.validate_status_code(response=response, expected_status_code=400)
    assertions.validate_json_schema_pydantic(json=response.json(), model=login.SchemaLoginErrorCase)


def test_login_with_special_characters_in_password(client, assertions, config, users_data):
    method = "POST"
    url = f"{config.base_url}/users/login"
    special_password = "P@$$w0rd!#$%^&*()_+-=[]{}|;':\",./<>?"
    json = users_data.get_payload_to_login(email=config.logged_in_email, password=special_password)

    response = client.send_request(method=method, url=url, json=json)

    assertions.validate_status_code(response=response, expected_status_code=400)
    assertions.validate_json_schema_pydantic(json=response.json(), model=login.SchemaLoginErrorCase)