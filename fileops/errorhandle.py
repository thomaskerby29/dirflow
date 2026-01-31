import pyuac

def invalid_command(command):
    print(str(command) + " is not a valid command")

def invalid_argument(command):
    print(str(command) + " is not a valid argument")

def missing_command(missing):
    print("Missing " + str(missing))

def unknown_error(error):
    print(str(error))
    print("A problem occurred\nIf the issue persists please create an issue")
    print("https://github.com/thomaskerby29/dirflow/issues")

def permission_error(path, operation, type):
    print("You dont have permission to perform " + str(operation) + " on " + str(path))
    if not pyuac.isUserAdmin():
        print("Try admin mode")
    else:
        print("This " + str(type) + " is protected")

def file_not_found(path):
    print(str(path) + " does not exist")

def folder_not_found(path):
    print(str(path) + " does not exist")

def os_error(error):
    print(error)
    print("Operating system error")

def value_error(where, vType, intended):
    print("Invalid input in " + str(where))
    print(str(vType) + " should be " + str(intended))

def out_of_range(min, max, user):
    print("You entered: " + str(user) + "\nValue needs to be: "+ str(min) + " - " + str(max))