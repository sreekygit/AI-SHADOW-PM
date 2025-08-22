# Utility functions for loading signals

def load_signals(path="signals.json"):
    import json
    with open(path, "r") as f:
        return json.load(f)
