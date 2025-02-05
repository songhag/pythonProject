#lab5.py

# Starter code for lab 5 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.
# Please see the README in this repository for the requirements of this lab exercise

# Songhao Gao
# songhag@uci.edu
# 42515328

from pathlib import Path

# ---------------------

class Note:
    def __init__(self, path: Path):
        self.path = path
        self.notes = self.read_notes()

    def read_notes(self):
        if not self.path.exists():
            return []
        with open(self.path, 'r') as file:
            return [line.strip() for line in file.readlines()]

    def save_note(self, note: str):
        with open(self.path, 'a') as file:
            file.write(note + '\n')
        self.notes.append(note)

    def remove_note(self, index: int):
        if 0 <= index < len(self.notes):
            removed_note = self.notes.pop(index)
            self.save_all_notes()
            return removed_note
        raise IndexError("Note index out of range")

    def save_all_notes(self):
        with open(self.path, 'w') as file:
            for note in self.notes:
                file.write(note + '\n')


# ---------------------

NOTES_PATH = "."
NOTES_FILE = "pynote.txt"


def print_notes(notes:list[str]):
    id = 0
    for n in notes:
        print(f"{id}: {n}")
        id+=1

def delete_note(note:Note):
    try:
        remove_id = input("Enter the number of the note you would like to remove: ")
        remove_note = note.remove_note(int(remove_id))
        print(f"The following note has been removed: \n\n {remove_note}")
    except FileNotFoundError:
        print("The PyNote.txt file no longer exists")
    except ValueError:
        print("The value you have entered is not a valid integer")

def run():
    p = Path(NOTES_PATH) / NOTES_FILE
    if not p.exists():
        p.touch()
    note = Note(p)
    
    print("Here are your notes: \n")
    print_notes(note.read_notes())

    user_input = input("Please enter a note (enter :d to delete a note or :q to exit):  ")

    if user_input == ":d":
        delete_note(note)
    elif user_input == ":q":
        return
    else:    
        note.save_note(user_input)
    run()


if __name__ == "__main__":
    print("Welcome to PyNote! \n")

    run()
