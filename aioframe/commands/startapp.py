import os

from ..exceptions import AppCommandError


def create_folders(path, folders):
    for folder in folders:
        os.makedirs(os.path.join(path, folder))


def create_files(path, files):
    for filename, content in files.items():
        with open(os.path.join(path, filename), 'x') as created_file:
            created_file.write(content)


def run_command(conf, app_name):
    app_path = os.path.join(conf.APPS_DIR, app_name)
    if os.path.exists(app_path):
        raise AppCommandError('Could not create app at {}, already exists'.format(app_path))
    os.makedirs(app_path)
    app_folders = [
        'templates',
    ]
    app_files = {
        '__init__.py': "import sys\nfrom aioframe.loaders import get_app_modules\n\nsys.path.insert(0,'..')\n\n__all__ = get_app_modules(__name__)\n",
        'app_conf.py': "from aioframe.apps import AppConf\n\napp = AppConf('{app_name}', namespace='{app_name}')\n".format(app_name=app_name),
        'views.py': "# Views\n"
    }
    create_folders(app_path, app_folders)
    create_files(app_path, app_files)
    print("App {} created.".format(app_name))
