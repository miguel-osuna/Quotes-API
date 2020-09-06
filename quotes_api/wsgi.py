import os
from myapi.app import create_app

app = create_app(configuration=os.getenv("APP_CONFIGURATION", "ProductionConfig"))
