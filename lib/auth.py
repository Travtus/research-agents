"""
API Key Authentication Utility
"""

import os


def validate_api_key(request_handler) -> bool:
    """
    Validate API key from request headers
    
    Checks for API key in:
    1. X-API-Key header
    2. Authorization: Bearer <key> header
    
    Args:
        request_handler: HTTP request handler with headers
        
    Returns:
        bool: True if API key is valid, False otherwise
    """
    # Get the expected API key from environment
    expected_key = os.getenv('API_KEY')
    
    # If no API_KEY is set in environment, skip authentication
    # This allows the API to work without auth if not configured
    if not expected_key:
        return True
    
    # Check X-API-Key header
    api_key = request_handler.headers.get('X-API-Key')
    
    # If not found, check Authorization header
    if not api_key:
        auth_header = request_handler.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            api_key = auth_header.replace('Bearer ', '')
    
    # Validate the key
    return api_key == expected_key


def send_unauthorized_response(request_handler):
    """
    Send 401 Unauthorized response
    
    Args:
        request_handler: HTTP request handler
    """
    import json
    
    request_handler.send_response(401)
    request_handler.send_header('Content-Type', 'application/json')
    request_handler.send_header('Access-Control-Allow-Origin', '*')
    request_handler.send_header('WWW-Authenticate', 'Bearer realm="API"')
    request_handler.end_headers()
    
    response = {
        'success': False,
        'error': 'Unauthorized - Invalid or missing API key',
        'message': 'Please provide a valid API key in the X-API-Key header or Authorization: Bearer header'
    }
    
    request_handler.wfile.write(json.dumps(response).encode())

