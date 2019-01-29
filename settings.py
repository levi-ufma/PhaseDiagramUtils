# settings.py
import os
from dotenv import load_dotenv
from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Configs
apiKey = os.getenv("MAPI_KEY")