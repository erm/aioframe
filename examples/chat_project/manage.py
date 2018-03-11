import sys

from aioframe.commands import startapp, runapp, createsuperuser, createdb, dropdb

import conf


if __name__ == "__main__":
    sys_args = sys.argv[1:]
    command = sys_args[0]
    if command == 'startapp':
        app_name = sys_args[1]
        startapp.run_command(conf, app_name)
    if command == 'runapp':
        runapp.run_command(conf)
    if command == 'createsuperuser':
        username = sys_args[1]
        password = sys_args[2]
        createsuperuser.run_command(conf, username, password)
    if command == 'createdb':
        createdb.run_command(conf)
    if command == 'dropdb':
        dropdb.run_command(conf)

# TODO: Improve the command structure generally and generate manage file in project
