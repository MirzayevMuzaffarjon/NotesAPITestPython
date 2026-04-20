def test_register_valid_user(client, config):
    method = "POST"
    url = f"{config.base_url}/users/register"