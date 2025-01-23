import shlex

command = "grep -i 'hello world' file.txt"
tokens = shlex.split(command)

print("Command:", tokens[0])
print("Arguments:", tokens[1:])