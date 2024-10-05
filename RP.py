import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    # Remove if pyinstalling
    if relative_path.endswith(".png"):
        relative_path = (f"Graphics/{relative_path}")
    return os.path.join(base_path, relative_path)