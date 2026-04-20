def test_register_valid_user(client, config, users_data):
    method = "POST"
    url = f"{config.base_url}/users/register"
    payload = users_data.get_payload_to_register(name="Name Test auto", email=config.un_auth_email, password="Password")