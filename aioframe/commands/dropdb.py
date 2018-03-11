from ..loaders import get_apps_enabled, get_app_models
from ..auth.models import User, UserPermission # TODO: load these from conf


def run_command(conf):
    apps_enabled = get_apps_enabled(conf.APPS_REGISTRY)
    app_models = get_app_models(apps_enabled)
    app_models += [User, UserPermission]
    database = conf.DATABASE
    if app_models:
        database.drop_tables(app_models)
        print('Tables dropped.')
    else:
        print('No models provided.')
