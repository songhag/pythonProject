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
    if len(instruction) !=4:
        print("ERROR")
        main()
        return

    file=instruction[1]
    file=file.strip('"')
    file=Path(NOTES_PATH)/Path(file)
    if not file.exists() or not file.is_dir():
        print("ERROR")
        main()
        return

    if instruction[2]== '-n':
        file=file / Path(instruction[3]+EXTENSION)
    p = file

    if p.exists():
        print("ERROR")
    else:
        p.touch()
        print(p)


    main()

def delete_file(instruction):
    if len(instruction) !=2:
        print("ERROR")
        main()
        return
    path = Path(NOTES_PATH)/Path(instruction[1].strip('"'))

    if not path.exists():
        print("ERROR")
        main()
        return

    if path.suffix != '.dsu':
        print("ERROR")
        main()
        return

    try:
        path.unlink()
        print(f"{path} DELETED")
    except FileNotFoundError:
        print(f"ERROR")
        print(path)

    main()

def read_content(instruction):
    if len(instruction) !=2:
        print("ERROR")
        main()
        return

    path = Path(NOTES_PATH) / Path(instruction[1].strip('"'))

    if not path.exists():
        print("ERROR")
        main()
        return

    if path.suffix != '.dsu':
        print("ERROR")
        main()
        return

    if path.stat().st_size == 0:
        print("EMPTY")
        main()
        return

    try:
        with path.open('r') as file:
            for line in file:
                print(line.strip())
    except Exception as e:
        print(e)
        main()
        return

    main()

def main():
    instruction=input()
    instruction=instruction.replace('\\', '\\\\')
    instruction_split=shlex.split(instruction)
    command=instruction_split[0].upper()
    if command in COMMAND:
        COMMAND[command](instruction_split)
    else:
        print("ERROR")
        main()
        return
    return


if __name__ == "__main__":
    COMMAND={
        'C':create_new_file,
        'D':delete_file,
        'R':read_content,
        'Q':quit_the_program
    }
    main()