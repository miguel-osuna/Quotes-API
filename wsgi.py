import os
from quotes_api.app import create_app

app = create_app(configuration=os.getenv("APP_CONFIGURATION", "production"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8000")
