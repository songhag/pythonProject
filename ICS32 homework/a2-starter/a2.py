# a2.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Songhao Gao
# songhag@uci.edu
# 42515328

import Profile
import ui
import shlex
from pathlib import Path


NOTES_PATH = "."
EXTENSION = ".dsu"


def quit_the_program(instruction):
    return 0


def create_new_file(instruction):
    if len(instruction) != 4:
        print("ERROR")
        return

    file = instruction[1]
    file = file.strip('"')
    file = Path(NOTES_PATH)/Path(file)
    if not file.exists() or not file.is_dir():
        print("ERROR")
        return

    if instruction[2] == '-n':
        file = file / Path(instruction[3]+EXTENSION)
    p = file

    if p.exists():
        print("ERROR")
    else:
        p.touch()
        print(p)



def delete_file(instruction):
    if len(instruction) != 2:
        print("ERROR")
        return
    path = Path(NOTES_PATH) / Path(instruction[1].strip('"'))

    if not path.exists():
        print("ERROR")
        return

    if path.suffix != '.dsu':
        print("ERROR")
        return

    try:
        path.unlink()
        print(f"{path} DELETED")
    except FileNotFoundError:
        print(f"ERROR")
        print(path)



def read_content(instruction):
    if len(instruction) != 2:
        print("ERROR")
        return

    path = Path(NOTES_PATH) / Path(instruction[1].strip('"'))

    if not path.exists():
        print("ERROR")
        return

    if path.suffix != '.dsu':
        print("ERROR")
        return

    if path.stat().st_size == 0:
        print("EMPTY")
        return

    try:
        with path.open('r') as file:
            for line in file:
                print(line.strip())
    except Exception as e:
        print(e)
        return

COMMAND = {
    'C': create_new_file,
    'D': delete_file,
    'R': read_content,
    'Q': quit_the_program
}


def main():
    instruction = ui.introduction()
    instruction = instruction.replace('\\', '\\\\')
    instruction_split = shlex.split(instruction)
    command = instruction_split[0].upper()
    if command in COMMAND:
        temp = COMMAND[command](instruction_split)
        if temp != 0:
            main()
    else:
        print("ERROR")
        main()
        return
    return



if __name__ == "__main__":
    main()