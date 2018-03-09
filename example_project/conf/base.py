import os

from aiohttp import web

from aioframe.loaders import get_apps_enabled, load_apps_enabled


APPS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

APPS_REGISTRY = (
    'example_app',
    # 'example_app_two',
)

APPS_ENABLED = get_apps_enabled(APPS_REGISTRY)

webapp = web.Application()

load_apps_enabled(APPS_ENABLED, webapp)
