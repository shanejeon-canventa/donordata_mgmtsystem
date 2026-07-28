# configuration loader
import json
from pathlib import Path

def load_config_data(config_file_name: str = 'conf.json', data_dir: str = 'inputs') -> dict:
    """Reads runtime settings and path variables from JSON configuration file.
    
    Falls back to the local inputs directory if no alternative path is specified.
    """
    config_path = Path(data_dir) / config_file_name
    
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file missing: {config_path}")
    
    with open(config_path, mode='r', encoding='utf-8') as stream:
        return json.load(stream)
    