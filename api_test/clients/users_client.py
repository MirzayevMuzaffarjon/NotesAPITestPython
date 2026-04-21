import logging
from requests import Response, Session
from api_test.clients.base_client import BaseClient


class UsersClient(BaseClient):
    def __init__(self, session: Session = None, base_url: str = None):
        super().__init__(session=session)
        self.base_url = base_url
    
    def register(self, name: str, email: str, password: str) -> Response:
        """Register a new user"""
        url = f"{self.base_url}/users/register"
        data = {"name": name, "email": email, "password": password}
        return self.send_request(method="POST", url=url, data=data)
    
    def login(self, email: str, password: str) -> Response:
        """Login with existing user credentials"""
        url = f"{self.base_url}/users/login"
        data = {"email": email, "password": password}
        return self.send_request(method="POST", url=url, data=data)
    
    def delete_account(self, token: str) -> Response:
        """Delete the authenticated user account"""
        url = f"{self.base_url}/users/delete-account"
        headers = {"x-auth-token": token}
        return self.send_request(method="DELETE", url=url, headers=headers)
