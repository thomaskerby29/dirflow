from fileops.cleancmd import clean_cmd

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


while True:
    command = input(str("\nPlease enter a command: "))

    {'help': helpCommand,
     'clean': lambda: cleanCommand(command),
     'exit': lambda: exit()}[command.split(' ', 1)[0]]()