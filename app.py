"""
YouTube Learning Assistant - Main Application Entry Point
Organized with separate backend and frontend modules
"""

import sys
import os

# Add project root and subdirectories to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'frontend'))
sys.path.insert(0, os.path.join(project_root, 'backend'))

# Import and run the frontend UI
try:
    from frontend.ui import main
except ImportError:
    # Fallback for deployment environments
    from ui import main

if __name__ == "__main__":
    main()
