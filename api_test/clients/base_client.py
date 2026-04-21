"""Base API client for making HTTP requests."""
import logging
from typing import Optional, Any, Dict

import requests
from requests import Response, RequestException, Session


class BaseClient:
    """Base HTTP client for API testing."""
    
    DEFAULT_TIMEOUT = 30
    
    def __init__(self, base_url: str, session: Optional[Session] = None):
        """Initialize the base client.
        
        Args:
            base_url: Base URL for the API.
            session: Optional requests Session object.
        """
        self.base_url = base_url.rstrip('/')
        self.session = session or requests.Session()
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def send_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        timeout: int = DEFAULT_TIMEOUT
    ) -> Response:
        """Send an HTTP request.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint path (e.g., '/users/login')
            params: URL query parameters
            headers: HTTP headers
            json: JSON body data
            data: Form data
            files: Files to upload
            timeout: Request timeout in seconds
            
        Returns:
            Response object
            
        Raises:
            RequestException: If the request fails
        """
        url = f"{self.base_url}{endpoint}"
        self._log_request(method, url, params, headers, json, data, timeout)
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                headers=headers,
                json=json,
                data=data,
                files=files,
                timeout=timeout
            )
            
            self._log_response(response)
            return response
            
        except RequestException as e:
            self._log_error(e)
            raise
    
    def _log_request(
        self,
        method: str,
        url: str,
        params: Optional[Dict],
        headers: Optional[Dict],
        json: Optional[Dict],
        data: Optional[Dict],
        timeout: int
    ) -> None:
        """Log request details."""
        self.logger.info(f"--> {method.upper()} {url}")
        if params:
            self.logger.info(f"--> Params: {params}")
        if headers:
            self.logger.info(f"--> Headers: {headers}")
        if json:
            self.logger.info(f"--> JSON: {json}")
        if data:
            self.logger.info(f"--> Data: {data}")
        self.logger.info(f"--> Timeout: {timeout}s")
    
    def _log_response(self, response: Response) -> None:
        """Log response details."""
        self.logger.info(f"<-- Status: {response.status_code}")
        
        try:
            body = response.json()
            self.logger.info(f"<-- Body: {body}")
        except ValueError:
            body = response.text[:800]
            self.logger.info(f"<-- Body: {body}")
        
        if response.headers:
            self.logger.debug(f"<-- Headers: {dict(response.headers)}")
    
    def _log_error(self, error: RequestException) -> None:
        """Log request error details."""
        self.logger.error(f"❌ Request failed: {error}")
        if hasattr(error, 'response') and error.response is not None:
            self.logger.error(f"<-- Status: {error.response.status_code}")
            self.logger.error(f"<-- Body: {error.response.text[:800]}")