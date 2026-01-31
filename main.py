from fileops.cleancmd import clean_cmd
import pyuac
import sys

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

while True:
    try:
        command = input(str(f"\ndirflow{symbol} "))

        {'help': helpCommand,
         'clean': lambda: cleanCommand(command),
         'exit': lambda: sys.exit(),
         'admin': lambda: adminCommand()}[command.split(' ', 1)[0]]()
    except Exception:
        print("Invalid command - type 'help' for help")