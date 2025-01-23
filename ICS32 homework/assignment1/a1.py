# Songhao Gao
# songhag@uci.edu
# 42515328

from pathlib import Path
import shlex

NOTES_PATH = "."
EXTENSION = ".dsu"

def quit_the_program(instruction):
    return

def create_new_file(instruction):
    file=instruction[1]
    file=file.strip('"')

    if not (Path(NOTES_PATH)/Path(file)).exists() or not (Path(NOTES_PATH)/Path(file)).is_dir():
        print("ERROR: file not found")
        return

    if instruction[2]== '-n':
        file+=instruction[3]+EXTENSION
    p = Path(NOTES_PATH) / file

    if p.exists():
        print("ERROR: file already exists")
    else:
        p.touch()

    main()

def delete_file(instruction):
    path = Path(NOTES_PATH)/Path(instruction[1].strip('"'))

    if not path.exists():
        print("ERROR: file not found")
        return

    if path.suffix != '.dsu':
        print("ERROR: not a DSU file.")
        return

    try:
        path.unlink()
        print(f"{path} DELETED\n")
    except FileNotFoundError:
        print(f"ERROR: file not found: {path}")

    main()

def read_content(instruction):
    path = Path(NOTES_PATH) / Path(instruction[1].strip('"'))

    if not path.exists():
        print("ERROR: file not found")
        return

    if path.suffix != '.dsu':
        print("ERROR: not a DSU file.")
        return

    if path.stat().st_size == 0:
        print("EMPTY")
        return

    try:
        with path.open('r') as file:
            for line in file:
                print(line.strip())
            print()
    except Exception as e:
        print(e)
        return

    main()

def main():
    print('Supported Commands\nC - Create a new file in the specified directory.\nD - Delete the file.\nR - Read the contents of a file.\nQ- Quit the program.\n')
    instruction=input()
    print()
    instruction_split=shlex.split(instruction)
    command=instruction_split[0].upper()
    COMMAND[command](instruction_split)

    return


if __name__ == "__main__":
    COMMAND={
        'C':create_new_file,
        'D':delete_file,
        'R':read_content,
        'Q':quit_the_program
    }
    main()