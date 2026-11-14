import os
from dotenv import load_dotenv

load_dotenv()


BASE_URL = os.getenv("BASE_URL")
API_USERNAME = os.getenv("API_USERNAME")
API_PASSWORD = os.getenv("API_PASSWORD")


if not BASE_URL:
	raise ValueError("BASE_URL is not configured")