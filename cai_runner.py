#!/usr/bin/env python3
"""
Simple runner script for cai CLI when pip install is not available
"""

import sys
import os

# Add the current directory to Python path so we can import cai
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cai.cli import main

if __name__ == "__main__":
    sys.exit(main())
