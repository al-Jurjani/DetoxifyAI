"""
Pytest configuration file to fix import paths
This ensures app/main.py can import from rag_pipeline and guardrails
"""

import sys
from pathlib import Path

# Add app directory to sys.path so 'from rag_pipeline import' works
app_dir = Path(__file__).parent.parent / "app"
sys.path.insert(0, str(app_dir))
