"""
Vercel Serverless Function Handler for Vishnu AI
Fixed for FUNCTION_INVOCATION_FAILED error
"""
import sys
import os
from io import BytesIO

# Set Vercel environment FIRST - before any imports
os.environ['VERCEL'] = '1'
os.environ['TMPDIR'] = '/tmp'

# Add parent directory to Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Now import Flask app
try:
    from app import app, init_db
    # Initialize database
    try:
        init_db()
    except Exception:
        # Will init on first request
        pass
except Exception as e:
    # Fallback error handler
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def error():
        return f'App Import Error: {str(e)}', 500

def handler(request):
    """
    Vercel serverless function handler
    Handles request object from Vercel Python runtime
    """
    try:
        # Get request attributes
        method = getattr(request, 'method', 'GET')
        path = getattr(request, 'path', '/')
        query_string = getattr(request, 'query_string', '') or ''
        headers = dict(getattr(request, 'headers', {}))
        body = getattr(request, 'body', b'') or b''
        
        # Build WSGI environ
        environ = {
            'REQUEST_METHOD': method,
            'PATH_INFO': path,
            'SCRIPT_NAME': '',
            'QUERY_STRING': query_string,
            'CONTENT_TYPE': headers.get('Content-Type', ''),
            'CONTENT_LENGTH': str(len(body)),
            'SERVER_NAME': 'localhost',
            'SERVER_PORT': '443',
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'https',
            'wsgi.input': BytesIO(body) if body else BytesIO(),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': True,
            'wsgi.run_once': False,
        }
        
        # Add HTTP headers
        for key, value in headers.items():
            http_key = 'HTTP_' + key.upper().replace('-', '_')
            environ[http_key] = value
        
        # Response storage
        status_code = [200]
        response_headers = []
        
        def start_response(status, headers_list):
            status_code[0] = int(status.split()[0])
            response_headers[:] = headers_list
        
        # Execute Flask app
        response_iter = app(environ, start_response)
        
        # Collect response
        response_body = b''
        for chunk in response_iter:
            if isinstance(chunk, bytes):
                response_body += chunk
            else:
                response_body += chunk.encode('utf-8')
        
        # Return Vercel response format
        return {
            'statusCode': status_code[0],
            'headers': dict(response_headers),
            'body': response_body.decode('utf-8', errors='ignore')
        }
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/plain; charset=utf-8'},
            'body': f'Handler Error: {str(e)}\n\n{error_trace}'
        }
