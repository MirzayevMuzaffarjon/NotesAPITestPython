import pytest
from api_test.schemas.users.register import SchemaRegisterSuccess, SchemaRegisterErrorCase
from api_test.clients.users_client import UsersClient


@pytest.fixture(scope="function")
def users_client(config):
    """Create a UsersClient instance for each test"""
    return UsersClient(base_url=config.base_url)


class TestUserRegistration:
    """Test suite for user registration endpoint"""
    
    def test_register_valid_user(self, users_client, assertions, users_data):
        """Test registering a new user with valid credentials"""
        # Generate unique user data to avoid conflicts
        name = users_data.get_test_user_name()
        email = users_data.generate_unique_email()
        password = "TestPassword123!"
        
        # Register the user
        response = users_client.register(name=name, email=email, password=password)
        
        # Validate response
        assertions.validate_status_code(response=response, expected_status_code=201)
        validated_data = assertions.validate_json_schema_pydantic(
            json=response.json(), 
            model=SchemaRegisterSuccess
        )
        
        # Verify returned data matches input
        assert validated_data.data.name == name
        assert validated_data.data.email == email
        
        # Cleanup: Login and delete the created account
        login_response = users_client.login(email=email, password=password)
        if login_response.status_code == 200:
            token = login_response.json()["data"]["token"]
            delete_response = users_client.delete_account(token=token)
            assertions.validate_status_code(response=delete_response, expected_status_code=200)
    
    def test_register_duplicate_email(self, users_client, assertions, users_data):
        """Test registering with an already existing email should fail"""
        # First registration
        name1 = users_data.get_test_user_name()
        email = users_data.generate_unique_email()
        password = "TestPassword123!"
        
        response1 = users_client.register(name=name1, email=email, password=password)
        assertions.validate_status_code(response=response1, expected_status_code=201)
        
        try:
            # Second registration with same email
            name2 = users_data.get_test_user_name()
            response2 = users_client.register(name=name2, email=email, password=password)
            
            # Should fail with 409 (Conflict) as per API behavior
            assertions.validate_status_code(response=response2, expected_status_code=409)
            assertions.validate_json_schema_pydantic(
                json=response2.json(), 
                model=SchemaRegisterErrorCase
            )
        finally:
            # Cleanup: Login and delete the created account
            login_response = users_client.login(email=email, password=password)
            if login_response.status_code == 200:
                token = login_response.json()["data"]["token"]
                delete_response = users_client.delete_account(token=token)
                assertions.validate_status_code(response=delete_response, expected_status_code=200)
    
    def test_register_missing_name(self, users_client, assertions, config):
        """Test registering without name should fail"""
        email = "test@example.com"
        password = "TestPassword123!"
        
        url = f"{config.base_url}/users/register"
        data = {"email": email, "password": password}
        
        response = users_client.send_request(method="POST", url=url, data=data)
        
        assertions.validate_status_code(response=response, expected_status_code=400)
        assertions.validate_json_schema_pydantic(
            json=response.json(), 
            model=SchemaRegisterErrorCase
        )
    
    def test_register_missing_email(self, users_client, assertions, config, users_data):
        """Test registering without email should fail"""
        name = users_data.get_test_user_name()
        password = "TestPassword123!"
        
        url = f"{config.base_url}/users/register"
        data = {"name": name, "password": password}
        
        response = users_client.send_request(method="POST", url=url, data=data)
        
        assertions.validate_status_code(response=response, expected_status_code=400)
        assertions.validate_json_schema_pydantic(
            json=response.json(), 
            model=SchemaRegisterErrorCase
        )
    
    def test_register_missing_password(self, users_client, assertions, config, users_data):
        """Test registering without password should fail"""
        name = users_data.get_test_user_name()
        email = users_data.generate_unique_email()
        
        url = f"{config.base_url}/users/register"
        data = {"name": name, "email": email}
        
        response = users_client.send_request(method="POST", url=url, data=data)
        
        assertions.validate_status_code(response=response, expected_status_code=400)
        assertions.validate_json_schema_pydantic(
            json=response.json(), 
            model=SchemaRegisterErrorCase
        )
    
    def test_register_empty_payload(self, users_client, assertions, config):
        """Test registering with empty payload should fail"""
        url = f"{config.base_url}/users/register"
        data = {}
        
        response = users_client.send_request(method="POST", url=url, data=data)
        
        assertions.validate_status_code(response=response, expected_status_code=400)
        assertions.validate_json_schema_pydantic(
            json=response.json(), 
            model=SchemaRegisterErrorCase
        )
    
    def test_register_invalid_email_format(self, users_client, assertions, config, users_data):
        """Test registering with invalid email format should fail"""
        name = users_data.get_test_user_name()
        email = "invalid-email-format"
        password = "TestPassword123!"
        
        url = f"{config.base_url}/users/register"
        data = {"name": name, "email": email, "password": password}
        
        response = users_client.send_request(method="POST", url=url, data=data)
        
        assertions.validate_status_code(response=response, expected_status_code=400)
        assertions.validate_json_schema_pydantic(
            json=response.json(), 
            model=SchemaRegisterErrorCase
        )
    
    def test_register_short_password(self, users_client, assertions, config, users_data):
        """Test registering with very short password"""
        name = users_data.get_test_user_name()
        email = users_data.generate_unique_email()
        password = "123"  # Very short password
    
        url = f"{config.base_url}/users/register"
        data = {"name": name, "email": email, "password": password}
        
        response = users_client.send_request(method="POST", url=url, data=data)
        
        # May succeed or fail depending on API password requirements
        # If it succeeds, cleanup; if it fails, validate error
        if response.status_code == 201:
            # Cleanup if registration succeeded
            login_response = users_client.login(email=email, password=password)
            if login_response.status_code == 200:
                token = login_response.json()["data"]["token"]
                delete_response = users_client.delete_account(token=token)
                assertions.validate_status_code(response=delete_response, expected_status_code=200)
        else:
            assertions.validate_status_code(response=response, expected_status_code=400)
            assertions.validate_json_schema_pydantic(
                json=response.json(), 
                model=SchemaRegisterErrorCase
            )
    
    def test_register_special_characters_in_name(self, users_client, assertions, users_data):
        """Test registering with special characters in name"""
        name = "Test User @#$%^&*()"
        email = users_data.generate_unique_email()
        password = "TestPassword123!"
        
        response = users_client.register(name=name, email=email, password=password)
        
        # Should succeed as names can contain special characters
        if response.status_code == 201:
            assertions.validate_json_schema_pydantic(
                json=response.json(), 
                model=SchemaRegisterSuccess
            )
            # Cleanup
            login_response = users_client.login(email=email, password=password)
            if login_response.status_code == 200:
                token = login_response.json()["data"]["token"]
                delete_response = users_client.delete_account(token=token)
                assertions.validate_status_code(response=delete_response, expected_status_code=200)
        else:
            assertions.validate_status_code(response=response, expected_status_code=400)
    
    def test_register_very_long_name(self, users_client, assertions, users_data):
        """Test registering with very long name"""
        name = "A" * 500  # Very long name
        email = users_data.generate_unique_email()
        password = "TestPassword123!"
        
        response = users_client.register(name=name, email=email, password=password)
        
        # May succeed or fail depending on API limits
        if response.status_code == 201:
            # Cleanup if registration succeeded
            login_response = users_client.login(email=email, password=password)
            if login_response.status_code == 200:
                token = login_response.json()["data"]["token"]
                delete_response = users_client.delete_account(token=token)
                assertions.validate_status_code(response=delete_response, expected_status_code=200)
        else:
            assertions.validate_status_code(response=response, expected_status_code=400)
            assertions.validate_json_schema_pydantic(
                json=response.json(), 
                model=SchemaRegisterErrorCase
            )
    
    def test_register_sql_injection_in_name(self, users_client, assertions, users_data):
        """Test registering with SQL injection attempt in name"""
        name = "'; DROP TABLE users; --"
        email = users_data.generate_unique_email()
        password = "TestPassword123!"
        
        response = users_client.register(name=name, email=email, password=password)
        
        # Should be handled safely - either rejected or accepted without executing SQL
        if response.status_code == 201:
            # Cleanup if registration succeeded
            login_response = users_client.login(email=email, password=password)
            if login_response.status_code == 200:
                token = login_response.json()["data"]["token"]
                delete_response = users_client.delete_account(token=token)
                assertions.validate_status_code(response=delete_response, expected_status_code=200)
        else:
            assertions.validate_status_code(response=response, expected_status_code=400)
    
    def test_register_whitespace_only_name(self, users_client, assertions, config):
        """Test registering with whitespace only name should fail"""
        name = "   "
        email = "test_whitespace@example.com"
        password = "TestPassword123!"
        
        url = f"{config.base_url}/users/register"
        data = {"name": name, "email": email, "password": password}
        
        response = users_client.send_request(method="POST", url=url, data=data)
        
        assertions.validate_status_code(response=response, expected_status_code=400)
        assertions.validate_json_schema_pydantic(
            json=response.json(), 
            model=SchemaRegisterErrorCase
        )
