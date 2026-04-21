"""Users API client for user-related operations."""
from typing import Optional

from requests import Response, Session

from api_test.clients.base_client import BaseClient


class UsersClient(BaseClient):
    """Client for Users API endpoints."""
    
    def __init__(self, base_url: str, session: Optional[Session] = None):
        """Initialize the users client.
        
        Args:
            base_url: Base URL for the API.
            session: Optional requests Session object.
        """
        super().__init__(base_url=base_url, session=session)
    
    def register(self, name: str, email: str, password: str) -> Response:
        """Register a new user.
        
        Args:
            name: User's name.
            email: User's email address.
            password: User's password.
            
        Returns:
            Response object from the API.
        """
        data = {"name": name, "email": email, "password": password}
        return self.send_request(method="POST", endpoint="/users/register", data=data)
    
    def login(self, email: str, password: str) -> Response:
        """Login with existing user credentials.
        
        Args:
            email: User's email address.
            password: User's password.
            
        Returns:
            Response object from the API.
        """
        data = {"email": email, "password": password}
        return self.send_request(method="POST", endpoint="/users/login", data=data)
    
    def delete_account(self, token: str) -> Response:
        """Delete the authenticated user account.
        
        Args:
            token: Authentication token.
            
        Returns:
            Response object from the API.
        """
        headers = {"x-auth-token": token}
        return self.send_request(method="DELETE", endpoint="/users/delete-account", headers=headers)
