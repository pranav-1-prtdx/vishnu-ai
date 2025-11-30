"""
Vercel Serverless Function Handler
Compatible with Vercel Python runtime
"""
import sys
import os

# Set Vercel environment FIRST
os.environ['VERCEL'] = '1'
os.environ['TMPDIR'] = '/tmp'

# Add parent directory to path
parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent not in sys.path:
    sys.path.insert(0, parent)

# Import Flask app
try:
    from app import app, init_db
    # Initialize database on Vercel
    try:
        init_db()
    except:
        pass  # Will init on first request if needed
except ImportError as e:
    # Fallback if import fails
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def error():
        return f'Import Error: {str(e)}', 500

# Vercel handler function
def handler(request):
    """
    Vercel serverless function handler
    request object: method, path, headers, body, query_string
    """
    from io import BytesIO
    
    # Get request data
    method = request.method
    path = request.path
    query_string = getattr(request, 'query_string', '') or ''
    headers = dict(getattr(request, 'headers', {}))
    body = getattr(request, 'body', b'') or b''
    
    # Create WSGI environ
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
    
    # Response containers
    status_code = [200]
    response_headers = []
    
    def start_response(status, headers_list):
        status_code[0] = int(status.split()[0])
        response_headers[:] = headers_list
    
    # Call Flask app
    try:
        response_iter = app(environ, start_response)
        response_body = b''.join([
            chunk if isinstance(chunk, bytes) else chunk.encode('utf-8')
            for chunk in response_iter
        ])
        
        return {
            'statusCode': status_code[0],
            'headers': dict(response_headers),
            'body': response_body.decode('utf-8', errors='ignore')
        }
    except Exception as e:
        import traceback
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/plain'},
            'body': f'Error: {str(e)}\n{traceback.format_exc()}'
        }
