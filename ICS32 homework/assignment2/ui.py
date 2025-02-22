# ui.py
from turtledemo.sorting_animate import instructions1

# Starter code for assignment 2 in ICS
# 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Songhao Gao
# songhag@uci.edu
# 42515328

MODE = 0
COUNT = 0


def introduction():
    global MODE
    instruction = ''
    if MODE == 0:
        print("Welcome! Do you want to create "
              "or load a DSU file (type 'c' to create or ‘o' to load):")
        func = input()
        instruction = func
        if func.upper() == "ADMIN":
            MODE = 1
            return introduction()
        if func.upper() == "C":
            print("Great! What is the path?")
            path = input()
            sign = '-n'
            print('What is the file name?')
            name = input()
            instruction += ' ' + path + ' ' + sign + ' ' + name
        if func.upper() == "O":
            print("Great! What is the name of the"
                  " file you would like to load?")
            path = input()
            instruction += ' ' + path
    else:
        instruction = input()

    return instruction


def asking_profile():
    global MODE
    if MODE == 1:
        while True:
            name = input()
            if name.strip() == '':
                print('ERROR')
            else:
                break

        while True:
            password = input()
            if password.strip() == '':
                print('ERROR')
            else:
                break

        bio = input()
    else:
        print('username: a unique name to associate the '
              'user with posts.\npassword: a password to '
              'protect access to user journal entries.\n'
              'bio: a brief description of the user.')

        while True:
            name = input('Name:\n')
            if name.strip() == '':
                print('Username cannot be an empty string.')
            else:
                break

        while True:
            password = input('Password:\n')
            if password.strip() == '':
                print('Password cannot be an empty string.')
            else:
                break

        bio = input('Biography:\n')

    return [name, password, bio]


def existing_file(username, bio):
    global MODE
    if MODE != 1:
        print("The DSU file has been successfully loaded!\n")
        print(f"Username: {username}")
        print(f"Biography: {bio}\n")


def nothing_entered():
    global MODE
    if MODE != 1:
        print('Nothing entered!')


def success_create():
    global MODE
    if MODE != 1:
        print("The DSU file has been successfully created!\n")


def success_edit():
    global MODE
    if MODE != 1:
        print("The DSU file has been successfully edited!\n")


def wrong_command():
    global MODE
    if MODE == 1:
        print("ERROR")
    else:
        print("You entered wrong command! Please try again.")


def wrong_instruction():
    global MODE
    if MODE == 1:
        print("ERROR")
    else:
        print("You entered wrong instruction! Please try again.")


def file_not_exist():
    global MODE
    if MODE == 1:
        print("ERROR")
    else:
        print("File not exist or wrong path! Please try again.")


def file_already_exist():
    print("File already exists! Change to load file")


def wrong_id():
    global MODE
    if MODE == 1:
        print("ERROR")
    else:
        print("No such id! Please try again.")


def main_process():
    global MODE
    global COUNT
    if MODE != 1:
        print("Do you want to edit or print the DSU "
              "file (E for edit or P for print)?")
        if COUNT < 1:
            print('E options:')
            print('-usr | -pwd | -bio | -addpost | -delpost \n')
            print('P options:')
            print('-usr | -pwd | -bio | -posts | -post [ID] | -all \n')
    instruction = input()
    COUNT = COUNT + 1
    return instruction
