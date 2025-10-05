#!/usr/bin/env python3
"""AWS Cognito Authentication Helper"""

import os
import boto3
from typing import Optional

class CognitoAuth:
    def __init__(self):
        self.client = boto3.client('cognito-idp')
        self.user_pool_id = os.getenv('COGNITO_USER_POOL_ID')
        self.client_id = os.getenv('COGNITO_CLIENT_ID')
    
    def authenticate(self, username: str, password: str) -> Optional[dict]:
        """Authenticate user with Cognito"""
        try:
            response = self.client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': username,
                    'PASSWORD': password
                }
            )
            return response['AuthenticationResult']
        except Exception as e:
            print(f"Auth error: {e}")
            return None
    
    def verify_token(self, token: str) -> Optional[dict]:
        """Verify JWT token"""
        try:
            response = self.client.get_user(AccessToken=token)
            return response
        except Exception:
            return None
