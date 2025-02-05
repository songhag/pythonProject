# ui.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Songhao Gao
# songhag@uci.edu
# 42515328

MODE=0

def introduction():
    print("Welcome! Do you want to create or load a DSU file (type 'c' to create or ‘o' to load):")
    instruction = input()
    if instruction.upper() == "ADMIN":
        global MODE
        MODE = 1
    return instruction

