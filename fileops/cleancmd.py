import os
from pathlib import Path

def duplicate_cmd(parts):
    print("Coming Soon")


def older_cmd(parts):
    print("Coming soon")


def empty_cmd(parts):
    emptyFolders = []

    for f in Path(parts[1]).iterdir():
        if f.is_dir() and not any(f.iterdir()):
            emptyFolders.append(str(f))

    print("\nThe following folders will be removed:")
    for x in emptyFolders:
        print(x)

    if '--skip-confirm' in parts:
        folder_remove(emptyFolders)
    elif '--dry-run' in parts:
        pass
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


def clean_cmd(cmd):
    parts = cmd.split(' ')
    {'--duplicates': lambda: duplicate_cmd(parts),
     '--older-than': lambda: older_cmd(parts),
     '--empty-folders': lambda: empty_cmd(parts)}[parts[2]]()