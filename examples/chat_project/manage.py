import sys

from aioframe.commands import startapp, runapp

import conf


if __name__ == "__main__":
    sys_args = sys.argv[1:]
    command = sys_args[0]
    if command == 'startapp':
        arg = sys_args[1]
        startapp.run_command(conf, arg)
    if command == 'runapp':
        runapp.run_command(conf)

# TODO: Improve the command structure generally and generate manage file in project
