class UsersData:
    @staticmethod
    def get_payload_to_login(email: str, password: str):
        payload = {"email": email, "password": password}
        return payload