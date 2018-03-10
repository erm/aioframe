import sys

from aioframe.commands import startapp

import conf


if __name__ == "__main__":
    sys_args = sys.argv[1:]
    command = sys_args[0]
    arg = sys_args[1]
    # TODO: Allow more commands
    startapp.run_command(conf, arg)