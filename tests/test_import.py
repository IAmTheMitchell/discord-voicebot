import importlib
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

def test_import():
    assert importlib.import_module('voicebot') is not None
