import os
from pathlib import Path
import time
import hashlib
from fileops.errorhandle import *
import traceback


def duplicate_cmd(parts):
    BUF_SIZE = 65536
    allFiles = {}

    def check_all(folder):
        for f in folder.iterdir():
            if f.is_file():
                md5 = hashlib.md5()
                try:
                    with open(str(f), 'rb') as file:
                        while chunk := file.read(BUF_SIZE):
                            md5.update(chunk)
                        allFiles.setdefault(md5.hexdigest(), []).append(f)
                except PermissionError:
                    permission_error(str(f), "file read", "file")
            elif f.is_dir():
                if '--all-subfolders' in parts:
                    check_all(f)

    check_all(Path(parts[1]))

    removeArray = []
    print("Duplicate files:")
    for file_hash, file_list in allFiles.items():
        if len(file_list) > 1:
            for f in file_list:
                print(str(f))
                removeArray.append(str(f))
            if '--dry-run' in parts:
                print(file_hash)
            else:
                if '--skip-confirm' in parts:
                    print("Ignoring --skip-confirm")

                removeChoice = input("Select duplicate to keep (0-" + str(len(removeArray) - 1) + "): ")
                try:
                    removeChoice = int(removeChoice)
                    if type(removeChoice) == int:
                        del removeArray[int(removeChoice)]
                        file_remove(removeArray)
                        removeArray.clear()
                        print("Duplicate(s) removed")
                except IndexError:
                    out_of_range("0", str(len(removeArray)-1), str(removeChoice))
                except ValueError:
                    value_error("duplicate removal", type(removeChoice), "int")


def older_cmd(parts):
    allFiles = []
    oldFiles = []

    def check_all(folder):
        for f in folder.iterdir():
            if f.is_file():
                allFiles.append(str(f))
            elif f.is_dir():
                if '--all-subfolders' in parts:
                    check_all(f)

    check_all(Path(parts[1]))

    for x in allFiles:
        try:
            modify_time = (time.time() - os.path.getmtime(x)) / 86400
            if int(modify_time) > int(parts[3]):
                oldFiles.append(x)
        except PermissionError:
            permission_error(x, "read metadata", "file")
        except ValueError:
            value_error("file modify date", type(parts[3]), "int")
            break
        except IndexError:
            missing_command("days since file modification")
            break
    if len(oldFiles) == 0:
        return

    print("\nThe following files will be removed:")
    for x in oldFiles:
        print(x)
    if '--skip-confirm' in parts:
        file_remove(oldFiles)
    elif '--dry-run' in parts:
        print("No files were removed")
    else:
        confirm = input("Are you sure you want to remove these files? (Y/n): ")
        if confirm == 'Y':
            file_remove(oldFiles)
        else:
            print("Aborted")


def empty_cmd(parts):
    emptyFolders = []

    def check_empty(folder):
        for f in folder.iterdir():
            if f.is_dir():
                if '--all-subfolders' in parts:
                    check_empty(f)
                if not any(f.iterdir()):
                    emptyFolders.append(str(f))

    check_empty(Path(parts[1]))

    print("\nThe following folders will be removed:")
    for x in emptyFolders:
        print(x)

    if '--skip-confirm' in parts:
        folder_remove(emptyFolders)
    elif '--dry-run' in parts:
        print("No folders were removed")
    else:
        confirm = input("Are you sure you want to remove these folders? (Y/n): ")
        if confirm == 'Y':
            folder_remove(emptyFolders)
        else:
            print("Aborted")


def folder_remove(emptyFolders):
    try:
        for x in emptyFolders:
            os.rmdir(x)
        print("Folders removed")
    except PermissionError:
        permission_error(str(x), "folder removal", "folder")
    except NotADirectoryError:
        folder_not_found(str(x))
    except OSError:
        os_error(traceback.format_exc())

def file_remove(oldFiles):
    try:
        for x in oldFiles:
            os.remove(x)
        print("Files removed")
    except PermissionError:
        permission_error(str(x), "file removal", "file")
    except FileNotFoundError:
        file_not_found(str(x))
    except OSError:
        os_error(traceback.format_exc())


def clean_cmd(cmd):
    parts = cmd.split(' ')
    mods = ['--all-subfolders', '--dry-run', '--skip-confirm', '--exclude']
    args = {'--duplicates': lambda: duplicate_cmd(parts),
            '--older-than': lambda: older_cmd(parts),
            '--empty-folders': lambda: empty_cmd(parts)}
    invalidMods = [p for p in parts[3:] if p.startswith('--') and p not in mods]

    if len(parts) < 2:
        missing_command("path")
    elif not os.path.isdir(parts[1]):
        folder_not_found(parts[1])
    elif len(parts) < 3:
        missing_command("argument")
    elif parts[2] not in args:
        invalid_argument(parts[2])
    elif invalidMods:
        invalid_argument(invalidMods[0])
    else:
        args[parts[2]]()