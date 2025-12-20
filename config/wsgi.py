import os
import sys
from django.core.wsgi import get_wsgi_application

# Print environment information for debugging
print("="*50, file=sys.stderr)
print("Python version:", sys.version, file=sys.stderr)
print("Current directory:", os.getcwd(), file=sys.stderr)
print("Files in directory:", os.listdir('.'), file=sys.stderr)
print("="*50, file=sys.stderr)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    application = get_wsgi_application()
    print("WSGI application loaded successfully", file=sys.stderr)
except Exception as e:
    print(f"Error loading WSGI application: {str(e)}", file=sys.stderr)
    raise

app = application