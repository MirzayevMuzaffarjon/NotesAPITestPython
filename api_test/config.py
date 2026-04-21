"""Configuration settings for API tests."""
import os
from dotenv import load_dotenv


class Config:
    """Application configuration manager."""
    
    def __init__(self):
        load_dotenv()
        self._base_url = os.getenv("BASE_URL")
        self._logged_in_email = os.getenv("LOGGED_IN_EMAIL")
        self._logged_in_password = os.getenv("LOGGED_IN_EMAIL_PASSWORD")
        self._un_auth_email = os.getenv("UN_AUTH_EMAIL")
    
    @property
    def base_url(self) -> str:
        """Get the base API URL."""
        if not self._base_url:
            raise ValueError("BASE_URL environment variable is not set")
        return self._base_url.rstrip('/')
    
    @property
    def logged_in_email(self) -> str:
        """Get the logged-in user email."""
        if not self._logged_in_email:
            raise ValueError("LOGGED_IN_EMAIL environment variable is not set")
        return self._logged_in_email
    
    @property
    def logged_in_password(self) -> str:
        """Get the logged-in user password."""
        if not self._logged_in_password:
            raise ValueError("LOGGED_IN_EMAIL_PASSWORD environment variable is not set")
        return self._logged_in_password
    
    @property
    def un_auth_email(self) -> str:
        """Get the unauthorized email."""
        return self._un_auth_email
    
    @property
    def default_password(self) -> str:
        """Get the default test password."""
        return "TestPassword123!"


# API Endpoints constants
class APIEndpoints:
    """API endpoint paths."""
    HEALTH_CHECK = "/health-check"
    USERS_REGISTER = "/users/register"
    USERS_LOGIN = "/users/login"
    USERS_DELETE_ACCOUNT = "/users/delete-account"
    NOTES = "/notes"