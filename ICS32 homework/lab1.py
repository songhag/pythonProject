def calculation(num1,num2,operator):
    if operator=='+':
        return num1+num2
    if operator=='-':
        return num1-num2
    if operator=='x':
        return num1*num2

print('Welcome to ICS 32 PyCalc!')
print()
num1=int(input('Enter your first operand: '))
num2=int(input('Enter your second operand: '))
operator=input('Enter your desired operator (+, -, or x): ')
result=calculation(num1,num2,operator)
print()
print('The result of your calculation is:',result)