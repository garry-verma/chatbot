from app.main import app
from flask_cors import CORS

# Enable CORS for all routes
CORS(app)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
