import os
import sys

# Detect if inside a virtual environment
if sys.prefix == sys.base_prefix:
    print("⚠️ You are not inside a virtual environment. Consider using `pipenv shell` or `python -m venv venv`.")
else:
    print("✅ Virtual environment detected.")
