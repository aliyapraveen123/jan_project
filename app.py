"""
YouTube Learning Assistant - Main Application Entry Point
Organized with separate backend and frontend modules
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

# Import and run the frontend UI
from frontend.ui import main

if __name__ == "__main__":
    main()
