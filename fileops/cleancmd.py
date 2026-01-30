import os
from pathlib import Path
import time

def duplicate_cmd(parts):
    print("Coming Soon")


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
        modify_time = (time.time() - os.path.getmtime(x)) / 86400
        if int(modify_time) > int(parts[3]):
            oldFiles.append(x)
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
    for x in emptyFolders:
        os.rmdir(x)
    print("Folders removed")


def file_remove(oldFiles):
    for x in oldFiles:
        os.remove(x)
    print("Files removed")



def clean_cmd(cmd):
    parts = cmd.split(' ')
    {'--duplicates': lambda: duplicate_cmd(parts),
     '--older-than': lambda: older_cmd(parts),
     '--empty-folders': lambda: empty_cmd(parts)}[parts[2]]()