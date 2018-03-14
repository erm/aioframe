from importlib import import_module

import aiohttp_session

from .exceptions import AppImportError


def setup(webapp, conf):
    webapp['AIOFRAME_SETTINGS'] = {'AIOFRAME_CONF': conf, 'AIOFRAME_APPS': {}}
    aiohttp_session.setup(webapp, conf.SESSION_STORAGE)
    for app_name in conf.APPS_REGISTRY:
        try:
            app_module = import_module(app_name)
        except ImportError as e:
            raise AppImportError(e)
        app_module.apps.app.setup(webapp)
