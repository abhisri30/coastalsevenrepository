from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")
    cognito_user_pool_id: str = os.getenv("COGNITO_USER_POOL_ID", "us-east-1_CG0XAi9sJ")
    cognito_client_id: str = os.getenv("COGNITO_CLIENT_ID", "4a22v7bip15r7uth68c6h3d2bt")
    cognito_client_secret: str = os.getenv("COGNITO_CLIENT_SECRET", "am6tsqubtdmof79gai7onr0fpeofavml5hb8r0ankvuqvge2m4c")

settings = Settings()