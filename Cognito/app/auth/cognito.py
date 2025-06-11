import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException
from jose import jwt
import time
import hmac
import hashlib
import base64
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from app.config import settings

class CognitoClient:
    _instance = None

    def __new__(cls):
        """Ensure a singleton instance of CognitoClient."""
        if cls._instance is None:
            cls._instance = super(CognitoClient, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not getattr(self, '_initialized', False):
            self.client = boto3.client('cognito-idp', region_name=settings.aws_region)
            self.user_pool_id = settings.cognito_user_pool_id
            self.client_id = settings.cognito_client_id
            self.client_secret = settings.cognito_client_secret
            self._jwks = None
            self._jwks_last_fetched = 0
            self._jwks_cache_duration = 86400  
            self._revoked_tokens = set() 
            self._initialized = True
            logger.info("CognitoClient singleton initialized")

    def _get_secret_hash(self, username: str) -> str:
        """Compute the SECRET_HASH for Cognito requests."""
        if not self.client_secret:
            return None
        message = username + self.client_id
        dig = hmac.new(
            self.client_secret.encode('utf-8'),
            msg=message.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        return base64.b64encode(dig).decode('utf-8')

    def _hash_token(self, token: str) -> str:
        """Hash the token to store in revoked_tokens."""
        return hashlib.sha256(token.encode('utf-8')).hexdigest()

    def sign_up(self, username: str, password: str, email: str):
        try:
            auth_parameters = {
                'USERNAME': username,
                'PASSWORD': password,
                'SECRET_HASH': self._get_secret_hash(username)
            } if self.client_secret else {
                'USERNAME': username,
                'PASSWORD': password
            }
            response = self.client.sign_up(
                ClientId=self.client_id,
                Username=username,
                Password=password,
                UserAttributes=[
                    {'Name': 'email', 'Value': email},
                ],
                SecretHash=self._get_secret_hash(username) if self.client_secret else None
            )
            return response
        except ClientError as e:
            raise HTTPException(status_code=400, detail=str(e))

    def confirm_sign_up(self, username: str, confirmation_code: str):
        try:
            auth_parameters = {
                'USERNAME': username,
                'SECRET_HASH': self._get_secret_hash(username)
            } if self.client_secret else {
                'USERNAME': username
            }
            response = self.client.confirm_sign_up(
                ClientId=self.client_id,
                Username=username,
                ConfirmationCode=confirmation_code,
                SecretHash=self._get_secret_hash(username) if self.client_secret else None
            )
            return response
        except ClientError as e:
            raise HTTPException(status_code=400, detail=str(e))

    def sign_in(self, username: str, password: str):
        try:
            auth_parameters = {
                'USERNAME': username,
                'PASSWORD': password,
                'SECRET_HASH': self._get_secret_hash(username)
            } if self.client_secret else {
                'USERNAME': username,
                'PASSWORD': password
            }
            response = self.client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters=auth_parameters
            )
            return response['AuthenticationResult']
        except ClientError as e:
            raise HTTPException(status_code=401, detail=str(e))

    def sign_out(self, access_token: str):
        try:
            token_hash = self._hash_token(access_token)
            logger.info(f"Before sign-out: Total revoked tokens: {len(self._revoked_tokens)}")
            response = self.client.global_sign_out(
                AccessToken=access_token
            )
            self._revoked_tokens.add(token_hash)
            logger.info(f"Token hash added to revoked list: {token_hash[:20]}... (Total revoked tokens: {len(self._revoked_tokens)})")
            return response
        except ClientError as e:
            logger.error(f"Sign-out failed: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))

    def verify_token(self, token: str):
        try:
            # Check if token is in revoked list
            token_hash = self._hash_token(token)
            logger.info(f"Checking token hash: {token_hash[:20]}... against {len(self._revoked_tokens)} revoked tokens")
            if token_hash in self._revoked_tokens:
                logger.error(f"Token hash is revoked: {token_hash[:20]}...")
                raise HTTPException(status_code=401, detail="Invalid token: Token has been revoked")

            # Refresh JWKS if not cached or cache expired
            current_time = time.time()
            if not self._jwks or (current_time - self._jwks_last_fetched) > self._jwks_cache_duration:
                jwks_url = f"https://cognito-idp.{settings.aws_region}.amazonaws.com/{self.user_pool_id}/.well-known/jwks.json"
                logger.info(f"Fetching JWKS from {jwks_url}")
                response = requests.get(jwks_url)
                response.raise_for_status()
                self._jwks = response.json()
                self._jwks_last_fetched = current_time

            # Get token headers and find matching key
            headers = jwt.get_unverified_headers(token)
            kid = headers.get('kid')
            if not kid:
                logger.error("Token missing kid header")
                raise HTTPException(status_code=401, detail="Invalid token: Missing kid")

            key = next((k for k in self._jwks['keys'] if k['kid'] == kid), None)
            if not key:
                logger.error(f"No JWKS key found for kid: {kid}")
                raise HTTPException(status_code=401, detail="Invalid token: Key not found")

            unverified_payload = jwt.get_unverified_claims(token)
            logger.info(f"Unverified token payload: {unverified_payload}")
            payload = jwt.decode(
                token,
                key,
                algorithms=['RS256'],
                options={"verify_aud": False},  # Relax audience check
                issuer=f"https://cognito-idp.{settings.aws_region}.amazonaws.com/{self.user_pool_id}"
            )

            # Check expiration
            if payload['exp'] < time.time():
                logger.error("Token has expired")
                raise HTTPException(status_code=401, detail="Token has expired")

            logger.info(f"Token verified successfully: {payload}")
            return payload
        except requests.RequestException as e:
            logger.error(f"Failed to fetch JWKS: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to fetch JWKS: {str(e)}")
        except Exception as e:
            logger.error(f"Token verification failed: {str(e)}")
            raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")