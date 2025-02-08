import shlex

command = "grep -post [ID] 'hello world' file.txt"
tokens = shlex.split(command)

print("Command:", tokens[1].upper())
print("Arguments:", tokens[1:])