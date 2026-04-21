"""Test data generators and fixtures."""
import time


class UsersData:
    """User test data generator."""
    
    DEFAULT_PASSWORD = "TestPassword123!"
    
    @staticmethod
    def get_payload_to_login(email: str, password: str) -> dict:
        """Create login payload.
        
        Args:
            email: User email.
            password: User password.
            
        Returns:
            Dictionary with login credentials.
        """
        return {"email": email, "password": password}
    
    @staticmethod
    def get_payload_to_register(name: str, email: str, password: str) -> dict:
        """Create registration payload.
        
        Args:
            name: User name.
            email: User email.
            password: User password.
            
        Returns:
            Dictionary with registration data.
        """
        return {"name": name, "email": email, "password": password}
    
    @staticmethod
    def generate_unique_email(prefix: str = "autotest") -> str:
        """Generate a unique email for testing to avoid conflicts.
        
        Args:
            prefix: Email prefix before timestamp.
            
        Returns:
            Unique email address string.
        """
        timestamp = int(time.time() * 1000)
        return f"{prefix}_{timestamp}@testmail.com"
    
    @staticmethod
    def get_test_user_name() -> str:
        """Generate a unique test user name.
        
        Returns:
            Unique user name string.
        """
        timestamp = int(time.time() * 1000)
        return f"AutoTest User {timestamp}"
