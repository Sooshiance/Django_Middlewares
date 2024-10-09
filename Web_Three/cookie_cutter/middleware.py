import json
import logging
from datetime import timedelta

from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import datetime


logger = logging.getLogger(__name__)


class Web3CookieMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Retrieve the Web3 cookie if it exists.
        web3_cookie = request.COOKIES.get('web3_cookie', None)

        if web3_cookie:
            try:
                # Process the cookie value (e.g., decode it, validate it).
                web3_data = self.decode_web3_cookie(web3_cookie)
                
                # Check for token expiry
                if 'expiry' in web3_data and datetime.strptime(web3_data['expiry'], '%Y-%m-%dT%H:%M:%S') < datetime.now():
                    logger.warning("Web3 cookie has expired.")
                    request.web3_data = None
                else:
                    request.web3_data = web3_data
                
            except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"Failed to decode Web3 cookie: {e}")
                request.web3_data = None
                raise
        else:
            request.web3_data = None

    def process_response(self, request, response):
        # Set a new Web3 cookie if necessary.
        if hasattr(request, 'web3_data') and request.web3_data:
            try:
                response.set_cookie(
                    'web3_cookie',
                    self.encode_web3_cookie(request.web3_data),
                    max_age=300,    # Cookie expiration time in seconds.
                    httponly=True,  # Prevent JavaScript access.
                    secure=True,    # Use only over HTTPS.
                    samesite='Lax'  # Adjust based on your needs.
                )
            except (TypeError, ValueError) as e:
                logger.error(f"Failed to encode Web3 data into a cookie: {e}")
                raise
        
        return response

    def encode_web3_cookie(self, data):
        # Implement your encoding logic here (e.g., JSON encoding).
        try:
            data['expiry'] = (datetime.now() + timedelta(seconds=3600)).strftime('%Y-%m-%dT%H:%M:%S')
            return json.dumps(data)
        except (TypeError, ValueError) as e:
            logger.error(f"Encoding error: {e}")
            raise

    def decode_web3_cookie(self, cookie_value):
        # Implement your decoding logic here (e.g., JSON decoding).
        try:
            return json.loads(cookie_value)
        except json.JSONDecodeError as e:
            logger.error(f"Decoding error: {e}")
            raise 


class RoleBasedAccessControlMiddleware(MiddlewareMixin):
    def process_request(self, request):
        web3_cookie = request.COOKIES.get('web3_cookie', None)
        
        if web3_cookie:
            try:
                web3_data = self.decode_web3_cookie(web3_cookie)
                
                if 'expiry' in web3_data and datetime.strptime(web3_data['expiry'], '%Y-%m-%dT%H:%M:%S') < datetime.now():
                    logger.warning("Web3 cookie has expired.")
                    request.web3_data = None
                else:
                    request.web3_data = web3_data
                    
                    # Extract roles from the decoded cookie
                    roles = web3_data.get('roles', [])
                    
                    # Attach roles to the request object
                    request.user_roles = roles
                
            except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"Failed to decode Web3 cookie: {e}")
                request.web3_data = None
                raise
        else:
            request.web3_data = None
    
    def process_response(self, request, response):
        if hasattr(request, 'web3_data') and request.web3_data:
            try:
                response.set_cookie(
                    'web3_cookie',
                    self.encode_web3_cookie(request.web3_data),
                    max_age=3600,
                    httponly=True,
                    secure=True,
                    samesite='Lax'
                )
            except (TypeError, ValueError) as e:
                logger.error(f"Failed to encode Web4 data into a cookie: {e}")
                raise
        
        return response
    
    def encode_web4_cookie(self, data):
        try:
            data['expiry'] = (datetime.now() + timedelta(seconds=3600)).strftime('%Y-%m-%dT%H:%M:%S')
            return json.dumps(data)
        except (TypeError, ValueError) as e:
            logger.error(f"failed to encode Web4 data into a cookie: {e}")
