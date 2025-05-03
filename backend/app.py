import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables from .env
load_dotenv()

# Always use production config
app = create_app("production")

if __name__ == "__main__":
    # Never run debug mode in production
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=False)
