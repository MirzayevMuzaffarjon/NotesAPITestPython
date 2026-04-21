"""Users API client for user-related operations."""
from typing import Optional

from requests import Response, Session

from api_test.clients.base_client import BaseClient


class UsersClient(BaseClient):
    """Client for Users API endpoints."""
    
    def __init__(self, session: Optional[Session] = None, base_url: Optional[str] = None):
        """Initialize the users client.
        
        Args:
            session: Optional requests Session object.
            base_url: Base URL for the API.
        """
        super().__init__(session=session)
        if not base_url:
            raise ValueError("base_url is required")
        self.base_url = base_url.rstrip('/')
    
    def register(self, name: str, email: str, password: str) -> Response:
        """Register a new user.
        
        Args:
            name: User's name.
            email: User's email address.
            password: User's password.
            
        Returns:
            Response object from the API.
        """
        url = f"{self.base_url}/users/register"
        data = {"name": name, "email": email, "password": password}
        return self.send_request(method="POST", url=url, data=data)
    
    def login(self, email: str, password: str) -> Response:
        """Login with existing user credentials.
        
        Args:
            email: User's email address.
            password: User's password.
            
        Returns:
            Response object from the API.
        """
        url = f"{self.base_url}/users/login"
        data = {"email": email, "password": password}
        return self.send_request(method="POST", url=url, data=data)
    
    def delete_account(self, token: str) -> Response:
        """Delete the authenticated user account.
        
        Args:
            token: Authentication token.
            
        Returns:
            Response object from the API.
        """
        url = f"{self.base_url}/users/delete-account"
        headers = {"x-auth-token": token}
        return self.send_request(method="DELETE", url=url, headers=headers)
