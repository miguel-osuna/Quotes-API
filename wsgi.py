import os
from quotes_api.app import create_app

app = create_app(configuration=os.getenv("APP_CONFIGURATION", "production"))
