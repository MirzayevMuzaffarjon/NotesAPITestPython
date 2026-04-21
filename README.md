# API Test Automation Framework

A professional REST API test automation framework built with Python, pytest, and Pydantic. This project demonstrates best practices in API testing including modular architecture, schema validation, and comprehensive test coverage.

## 📋 Project Overview

This is a production-ready API testing framework designed for testing RESTful APIs. It features a clean, maintainable architecture with separation of concerns, making it easy to extend and scale.

### Key Features

- **Modular Architecture**: Clean separation of clients, tests, data, schemas, and utilities
- **Schema Validation**: Uses Pydantic for robust response schema validation
- **Soft Assertions**: Implements `pytest-check` for non-failing assertions that allow multiple validations per test
- **JSON Schema Validation**: Supports both traditional JSON Schema and Pydantic model validation
- **Logging**: Comprehensive request/response logging for debugging
- **Environment Configuration**: Dotenv-based configuration for different environments
- **Allure Reporting**: Integrated Allure test reporting for beautiful test documentation

## 🏗️ Project Structure

```
api_test/
├── clients/
│   └── base_client.py          # HTTP client wrapper with logging
├── config.py                   # Environment configuration loader
├── conftest.py                 # Pytest fixtures and hooks
├── data/
│   └── users.py                # Test data factories
├── schemas/
│   ├── health_check/
│   │   └── health_check_schemas.py
│   └── users/
│       └── login.py            # Pydantic models for response validation
├── tests/
│   ├── test_health_check/
│   │   └── test_health_check_api.py
│   ├── test_users/
│   │   ├── test_users_login.py
│   │   ├── test_users_register.py
│   │   └── test_profile.py
│   └── test_notes_crud/
│       └── test_notes_create.py
└── utils/
    └── assertions.py           # Custom assertion helpers
```

## 🛠️ Tech Stack

- **Python 3.x** - Core programming language
- **pytest** - Testing framework
- **Pydantic** - Data validation using Python type hints
- **requests** - HTTP library for API calls
- **pytest-check** - Soft assertions plugin
- **jsonschema** - JSON Schema validation
- **Allure** - Test reporting
- **python-dotenv** - Environment variable management

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd api_test
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API credentials:
   ```env
   BASE_URL="https://your-api-base-url.com"
   LOGGED_IN_EMAIL="your-test-email@example.com"
   LOGGED_IN_EMAIL_PASSWORD="your-test-password"
   UN_AUTH_EMAIL="unauthorized-email@example.com"
   ```

## 🚀 Running Tests

### Run all tests
```bash
pytest
```

### Run specific test file
```bash
pytest api_test/tests/test_health_check/test_health_check_api.py -v
```

### Run tests by keyword
```bash
pytest -k "login" -v
```

### Run with Allure reporting
```bash
pytest --alluredir=./allure-results
allure serve ./allure-results
```

### Run with verbose output
```bash
pytest -v -s
```

## 📝 Test Coverage

The framework includes tests for:

### Health Check API
- ✅ Verify health check endpoint returns 200 status
- ✅ Validate health check response structure and content

### Users API
- ✅ Login with valid credentials
- ✅ Login response data validation
- ✅ Login with incorrect password (401)
- ✅ Login with unauthorized email (401)
- ✅ Login with empty password (400)
- ✅ Login with empty email and password (400)
- ✅ Login with empty payload (400)
- ✅ User registration flow

### Notes CRUD API
- 🔄 Note creation tests (placeholder for expansion)

## 🔧 Framework Components

### BaseClient (`clients/base_client.py`)
A reusable HTTP client that wraps the `requests` library with built-in logging for all request/response details.

```python
client = BaseClient()
response = client.send_request(
    method="GET",
    url="https://api.example.com/endpoint",
    headers={"Authorization": "Bearer token"}
)
```

### Assertions (`utils/assertions.py`)
Custom assertion utilities for common validation patterns:

- `validate_status_code()` - HTTP status code validation
- `validate_json_schema()` - Traditional JSON Schema validation
- `validate_json_schema_pydantic()` - Pydantic model validation
- `validate_to_equality()` - Value equality checks

### Pydantic Schemas
Type-safe response models using Pydantic for robust validation:

```python
class SchemaLoginSuccess(BaseModel):
    success: bool
    status: int
    message: str
    data: Data
```

### Fixtures (`conftest.py`)
Session-scoped pytest fixtures for:
- `client` - HTTP client instance
- `assertions` - Assertion utilities
- `config` - Configuration object
- `users_data` - Test data factories

## 📊 Sample Test Example

```python
def test_login_valid_credentials(client, assertions, config, users_data):
    method = "POST"
    url = f"{config.base_url}/users/login"
    json = users_data.get_payload_to_login(
        email=config.logged_in_email, 
        password=config.logged_in_email_password
    )

    response = client.send_request(method=method, url=url, json=json)

    assertions.validate_status_code(response=response, expected_status_code=200)
    assertions.validate_json_schema_pydantic(
        json=response.json(), 
        model=login.SchemaLoginSuccess
    )
```

## 🎯 Best Practices Implemented

1. **Page Object Model (POM) Pattern** - Adapted for API testing with dedicated client layer
2. **Data-Driven Testing** - Separate test data from test logic
3. **Schema-First Validation** - Define expected response structures upfront
4. **Soft Assertions** - Continue test execution after assertion failures
5. **Comprehensive Logging** - Log all HTTP transactions for debugging
6. **Environment Separation** - Different configurations for different environments
7. **Type Safety** - Use Pydantic models for type-checked responses

## 🔐 Security Notes

- Never commit `.env` files with real credentials
- Use environment variables for sensitive data
- The `.env.example` file shows the required structure without secrets

## 📈 Future Enhancements

- [ ] Add more CRUD operations for Notes API
- [ ] Implement authentication token management
- [ ] Add database validation tests
- [ ] Integrate CI/CD pipeline configuration
- [ ] Add performance testing capabilities
- [ ] Expand test coverage for edge cases

## 🤝 Contributing

This is a portfolio project demonstrating API testing expertise. Feel free to use it as a reference for your own projects.

## 📄 License

This project is open source and available for educational purposes.

## 👤 Author

Created as a portfolio piece showcasing API test automation skills.

---

**Happy Testing! 🧪**
