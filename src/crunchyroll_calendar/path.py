import os
from pathlib import Path


path = Path(os.getenv('DATA_DIR', '.')).expanduser().absolute()
