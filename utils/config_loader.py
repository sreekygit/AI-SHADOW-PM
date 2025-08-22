# Utility functions for loading config

def load_config(path="config.yaml"):
    import yaml
    with open(path, "r") as f:
        return yaml.safe_load(f)
