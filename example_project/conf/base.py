import os
from importlib import import_module

from aioframe.loaders import get_apps_enabled


APPS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

APPS_REGISTRY = (
    'example_app',
)

APPS_ENABLED = get_apps_enabled(APPS_REGISTRY)

print(APPS_ENABLED)
