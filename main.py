from fileops.cleancmd import clean_cmd

print(r""" _____    _____   _____    ______   _         ____   __          __
|  __ \  |_   _| |  __ \  |  ____| | |       / __ \  \ \        / /
| |  | |   | |   | |__) | | |__    | |      | |  | |  \ \  /\  / / 
| |  | |   | |   |  _  /  |  __|   | |      | |  | |   \ \/  \/ /  
| |__| |  _| |_  | | \ \  | |      | |____  | |__| |    \  /\  /   
|_____/  |_____| |_|  \_\ |_|      |______|  \____/      \/  \/""")


def helpCommand():
    with open('cmdlist.txt', encoding='utf-8') as f:
        for line in f:
            print(line.rstrip('\n'))

def cleanCommand(cmd):
    clean_cmd(cmd)

command = input(str("\n\nWelcome to Dirflow!\nPlease enter a command: "))

{'help': helpCommand,
 'clean': lambda: cleanCommand(command)}[command.split(' ', 1)[0]]()