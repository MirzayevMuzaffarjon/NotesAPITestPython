import os
from dotenv import load_dotenv

class Config:
    load_dotenv()
    base_url = os.getenv("BASE_URL")
    logged_in_email = os.getenv("LOGGED_IN_EMAIL")
    logged_in_email_password = os.getenv("LOGGED_IN_EMAIL_PASSWORD")
    un_auth_email = os.getenv("UN_AUTH_EMAIL")