import sys
import os

# Ensure the app directory is in the system path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app import create_app # ✅ Explicit import

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
