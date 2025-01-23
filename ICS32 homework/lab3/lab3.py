#lab3.py

# Starter code for lab 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.
# Please see the README in this repository for the requirements of this lab exercise

# Songhao Gao
# songhag@uci.edu
# 42515328

from pathlib import Path

def print_exist_note(f):
    notes = f.readlines()
    print('Here are your notes: ')
    for i in notes:
        print(i, end='')

def asking_for_new_note(f):
    new_note = input('Please enter a new note (enter q to exit): ')
    while new_note != 'q':
        f.write(new_note + '\n')
        new_note = input('Please enter a new note (enter q to exit): ')

def run():
    file_path = Path("pynote.txt")
    try:
        with open(file_path, 'x+') as f:
            print_exist_note(f)
            asking_for_new_note(f)
    except FileExistsError:
        with open(file_path, 'r+') as f:
            print_exist_note(f)
            asking_for_new_note(f)

if __name__ == "__main__":
    print("Welcome to PyNote!")
    run()
