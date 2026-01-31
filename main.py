from fileops.cleancmd import clean_cmd
from fileops.errorhandle import *
import pyuac
import sys
import traceback

print(r""" _____    _____   _____    ______   _         ____   __          __
|  __ \  |_   _| |  __ \  |  ____| | |       / __ \  \ \        / /
| |  | |   | |   | |__) | | |__    | |      | |  | |  \ \  /\  / / 
| |  | |   | |   |  _  /  |  __|   | |      | |  | |   \ \/  \/ /  
| |__| |  _| |_  | | \ \  | |      | |____  | |__| |    \  /\  /   
|_____/  |_____| |_|  \_\ |_|      |______|  \____/      \/  \/""")
print("Welcome to Dirflow!")


def helpCommand():
    with open('cmdlist.txt', encoding='utf-8') as f:
        for line in f:
            print(line.rstrip('\n'))


def cleanCommand(cmd):
    clean_cmd(cmd)


def adminCommand():
    if not pyuac.isUserAdmin():
        print("Open as a new process")
        pyuac.runAsAdmin()
        sys.exit()


symbol = "#" if pyuac.isUserAdmin() else ">"
commands = {'help': helpCommand,
                'clean': lambda: cleanCommand(command),
                'exit': lambda: sys.exit(),
                'admin': lambda: adminCommand()
                }

while True:
    command = input(str(f"\ndirflow{symbol} "))

    try:
        if command.split(' ', 1)[0] not in commands:
            invalid_command(command.split(' ', 1)[0])
        else:
            commands[command.split(' ', 1)[0]]()
    except Exception:
        unknown_error(traceback.format_exc())
