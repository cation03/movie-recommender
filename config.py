import yaml
import os

def load_config(config_path="config.yml"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, config_path)
    with open(file_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config

config = load_config()
