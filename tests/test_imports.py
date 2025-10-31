import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import app.main


def test_import_main():
    assert hasattr(app.main, "app")
