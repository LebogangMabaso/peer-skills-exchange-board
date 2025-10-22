import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.api import app

if __name__ == '__main__':
    print("Starting server at http://localhost:5001")
    app.run(debug=True, port=5001)


