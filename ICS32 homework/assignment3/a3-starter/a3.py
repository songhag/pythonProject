# a3.py
from pickle import GLOBAL

from pyexpat.errors import messages

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Songhao Gao
# songhag@uci.edu
# 42515328

import Profile
import ui
import shlex
from pathlib import Path
import ds_client

NOTES_PATH = "."
EXTENSION = ".dsu"
PROFILE = Profile.Profile()
PATH = ''


def introduction_program():
    instruction = ui.introduction()
    instruction = instruction.replace('\\', '\\\\')
    instruction_split = shlex.split(instruction)

    if len(instruction_split) == 0:
        ui.nothing_entered()
        return introduction_program()

    command = instruction_split[0].upper()
    if command in COMMAND:
        temp = COMMAND[command](instruction_split)
        if temp == 0:
            return 0
    else:
        if command == 'ADMIN':
            print("ADMIN MODE")
        else:
            ui.wrong_command()
        return introduction_program()
    return


def quit_the_program(instruction):
    return 0


def create_new_file(instruction):
    global PATH
    if len(instruction) != 4:
        ui.wrong_instruction()
        return introduction_program()

    file = instruction[1]
    file = file.strip('"')
    file = Path(NOTES_PATH)/Path(file)
    if not file.exists() or not file.is_dir():
        ui.file_not_exist()
        return introduction_program()

    if instruction[2] == '-n':
        file = file / Path(instruction[3]+EXTENSION)
    else:
        ui.wrong_instruction()
        return introduction_program()
    p = file
    PATH = p

    return collect_profiles(p)


def delete_file(instruction):
    if len(instruction) != 2:
        ui.wrong_instruction()
        return introduction_program()
    path = Path(NOTES_PATH) / Path(instruction[1].strip('"'))

    if not path.exists():
        ui.file_not_exist()
        return introduction_program()

    if path.suffix != '.dsu':
        ui.file_not_exist()
        return introduction_program()

    try:
        path.unlink()
        print(f"{path} DELETED")
    except FileNotFoundError:
        ui.file_not_exist()
        print(path)
    return introduction_program()


def open_existing_file(instruction):
    global PROFILE
    global PATH

    if len(instruction) != 2:
        ui.wrong_instruction()
        return introduction_program()

    PATH = instruction[1]
    PROFILE = Profile.Profile()
    try:
        PROFILE.load_profile(PATH)
    except Exception as ex:
        print(f'The file is missing information or '
              f'not exist, please select another file: {ex}')
        return introduction_program()
    ui.existing_file(PROFILE.username, PROFILE.bio)

    return


def read_content(instruction):
    if len(instruction) != 2:
        ui.wrong_instruction()
        return introduction_program()

    path = Path(NOTES_PATH) / Path(instruction[1].strip('"'))

    if not path.exists():
        ui.file_not_exist()
        return introduction_program()

    if path.suffix != '.dsu':
        ui.file_not_exist()
        return introduction_program()

    if path.stat().st_size == 0:
        print("EMPTY")
        return introduction_program()

    try:
        with path.open('r') as file:
            for line in file:
                print(line.strip())
    except Exception as e:
        print(e)
        return introduction_program()

    return introduction_program()


def collect_profiles(path):
    global PROFILE

    if path.exists():
        ui.file_already_exist()
        PROFILE = Profile.Profile()

        try:
            PROFILE.load_profile(path)
        except Exception as ex:
            print(f'The file is missing information or not '
                  f'exist, please select another file: {ex}')
            return introduction_program()

        ui.existing_file(PROFILE.username, PROFILE.bio)

    else:
        profiles = ui.asking_profile()
        path.touch()
        print(path)
        PROFILE = Profile.Profile(username=profiles[0], password=profiles[1])
        PROFILE.bio = profiles[2]
        PROFILE.save_profile(path)
        ui.success_create()


def second_part():
    instruction = ui.main_process()
    instruction_split = shlex.split(instruction)

    if len(instruction_split) == 0:
        ui.nothing_entered()
        return second_part()

    command = instruction_split[0].upper()

    if len(instruction_split) == 1 and command != 'Q':
        ui.wrong_instruction()
        return second_part()

    if command in COMMAND2:
        temp = COMMAND2[command](instruction_split)
        if temp != 0:
            return second_part()
    else:
        ui.wrong_command()
        return second_part()

    return temp


def edit_profile(instruction):
    global PATH

    for i in range(1, len(instruction), 2):
        if instruction[i] in EDIT_COMMAND:
            EDIT_COMMAND[instruction[i]](instruction[i+1])
        else:
            ui.wrong_instruction()
            return 0

    PROFILE.save_profile(PATH)
    ui.success_edit()

    return


def print_profile(instruction):
    temp2=1

    if len(instruction) == 1:
        return

    if instruction[1] in PRINT_COMMAND:
        temp2=PRINT_COMMAND[instruction[1]](instruction)
    else:
        ui.wrong_instruction()
        return

    if temp2 == 0:
        return

    if instruction[1] == '-post' or instruction[1] == '-delpost':
        instruction.pop(2)

    instruction.pop(1)
    print_profile(instruction)
    return

def upload_profile(instruction):
    global PATH
    id=''
    if len(instruction) != 2:
        ui.wrong_instruction()
        return

    if instruction[1].isdigit():
        id=instruction[1]
    else:
        ui.wrong_instruction()
        return

    connect_upload_server(id=id)
    return

def connect_upload_server(id=None,new_bio=None):
    global PROFILE
    profile = PROFILE

    server = profile.dsuserver
    port = 3001
    username = profile.username
    password = profile.password
    bio = profile.bio
    post = profile._posts
    message=''
    if id is not None:
        if len(post) < int(id):
            ui.wrong_instruction()
            return
        message = post[int(id) - 1]['entry']

    if new_bio is not None:
        success = ds_client.send(server, port, username, password, message, bio=new_bio)
    else:
        success = ds_client.send(server, port, username, password, message, bio)

    if success:
        print("Message and bio sent successfully.\n")
    else:
        print("Failed to send message and bio.")
        return
    return

def edit_username(instruction):
    global PROFILE
    PROFILE.username = instruction
    return


def edit_password(instruction):
    global PROFILE
    PROFILE.password = instruction
    return


def edit_bio(instruction):
    global PROFILE
    PROFILE.bio = instruction

    print("Do you want to upload your bio? (enter Y or N)")
    upload=input()

    while True:
        if upload.upper() == 'Y':
            connect_upload_server(new_bio=instruction)
            return
        elif upload.upper() == 'N':
            return
        else:
            print("Please enter Y or N.")
            upload=input()
    return


def edit_add_post(instruction):
    global PROFILE
    post = Profile.Post(instruction)
    PROFILE.add_post(post)
    return


def edit_del_post(instruction):
    global PROFILE
    PROFILE.del_post(int(instruction)-1)
    return


def print_username(instruction):
    global PROFILE
    print(f'Username: {PROFILE.username}')
    return


def print_password(instruction):
    global PROFILE
    print(f'Password: {PROFILE.password}')
    return


def print_bio(instruction):
    global PROFILE
    print(f'Biography: {PROFILE.bio}')
    return


def print_posts(instruction):
    global PROFILE
    posts = PROFILE.get_posts()
    print(f'Posts:')
    id = 1
    for i in posts:
        print(f'{id}: {i.get_entry()}')
        id += 1
    print()
    return


def print_post_by_id(instruction):
    global PROFILE
    posts = PROFILE.get_posts()

    if len(instruction) <= 2:
        ui.wrong_instruction()
        return 0

    if not instruction[2].isdigit():
        ui.wrong_instruction()
        return 0

    if len(posts) < int(instruction[2]):
        ui.wrong_id()
        return 0
    print(f'Post{instruction[2]}: {posts[int(instruction[2])-1].get_entry()}')
    return


def print_all(instruction):
    print_username(instruction)
    print_password(instruction)
    print_bio(instruction)
    print_posts(instruction)
    return


COMMAND = {
    'C': create_new_file,
    'D': delete_file,
    'R': read_content,
    'Q': quit_the_program,
    'O': open_existing_file
}

COMMAND2 = {
    'Q': quit_the_program,
    'E': edit_profile,
    'P': print_profile,
    'U': upload_profile
}

EDIT_COMMAND = {
    '-usr': edit_username,
    '-pwd': edit_password,
    '-bio': edit_bio,
    '-addpost': edit_add_post,
    '-delpost': edit_del_post
}

PRINT_COMMAND = {
    '-usr': print_username,
    '-pwd': print_password,
    '-bio': print_bio,
    '-posts': print_posts,
    '-post': print_post_by_id,
    '-all': print_all
}


def main():
    temp = introduction_program()
    if temp == 0:
        return
    second_part()


if __name__ == "__main__":
    main()
    # E -addpost "Hello, this is my first post!"
    # P -all
    # P -post 1
