import os
from pathlib import Path


path = Path(os.getenv('DATA_DIR', '.')).expanduser().absolute()
username = os.getenv('CRUNCHYROLL_USERNAME')
password = os.getenv('CRUNCHYROLL_PASSWORD')