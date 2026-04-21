class UsersData:

    @staticmethod
    def get_payload_to_login(email: str, password: str):
        payload = {"email": email, "password": password}
        return payload
    
    @staticmethod
    def get_payload_to_register(name: str, email: str, password: str):
        payload = {"name": name, "email": email, "password": password}
        return payload
    
    @staticmethod
    def generate_unique_email(prefix: str = "autotest") -> str:
        """Generate a unique email for testing to avoid conflicts"""
        import time
        timestamp = int(time.time() * 1000)
        return f"{prefix}_{timestamp}@testmail.com"
    
    @staticmethod
    def get_test_user_name() -> str:
        """Generate a test user name"""
        import time
        timestamp = int(time.time() * 1000)
        return f"AutoTest User {timestamp}"
