# lab8v2.py

# Starter code for lab 8 in ICS 32
# Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Songhao Gao
# songhag@uci.edu
# 42515328


from abc import ABC, abstractmethod
import random


class Appetite:
    LOW = 3
    MEDIUM = 4
    HIGH = 5


class Dog(ABC):
    DEFAULT_APPETITE = None

    def __init__(self, name, age, appetite=None):
        self._name = name
        self._age = age
        self.hunger_clock = 0
        if appetite is None:
            self.appetite = self.DEFAULT_APPETITE
        else:
            self.appetite = appetite

    @abstractmethod

    def breed(self):
        pass

    def name(self):
        return self._name

    def age(self):
        return self._age

    def hungry(self):
        """
        The hungry method will check the hungry clock to see if some time has
        passed since the last feeding. If clock is greater than breed typical
        appetite, hunger assessment is randomly selected,
        otherwise hunger clock increases
        """
        if self.hunger_clock > self.appetite:
            return bool(random.getrandbits(1))
        else:
            self.hunger_clock += 1
            return False

    def feed(self):
        """
        Feeds the dog. Hunger clock is reset
        """
        self.hunger_clock = 0


class GermanShepherd(Dog):
    DEFAULT_APPETITE = Appetite.MEDIUM

    def breed(self):
        return "German Shepherd"


class Akita(Dog):
    DEFAULT_APPETITE = Appetite.LOW

    def breed(self):
        return "Akita"


class Shiba_Inu(Dog):
    DEFAULT_APPETITE = Appetite.LOW

    def breed(self):
        return "Shiba Inu"


if __name__ == "__main__":
    print("Select a dog breed:")
    print("1. German Shepherd")
    print("2. Akita")
    print("3. Shiba_Inu")
    choice = '4'
    while choice not in ["1", "2", "3"]:
        choice = input("Enter choice (1-3): ").strip()
        if choice == "1":
            breed_cls = GermanShepherd
        elif choice == "2":
            breed_cls = Akita
        elif choice == "3":
            breed_cls = Shiba_Inu

    while True:
        name = input("Enter your dog's name: ").strip()
        if name.strip() != '':
            break

    while True:
        age = input("Enter your dog's age: ").strip()
        if age.strip() != '' and age.isdigit():
            age = int(age)
            break

    dog = breed_cls(name, age)

    while True:
        is_hungry = dog.hungry()
        h_text = ""
        if is_hungry is False:
            h_text = "not "
        print(f"Your {dog.breed()}, {dog.name()} is {h_text}hungry.")
        feed = input(f"Would you like to feed {dog.name()}? (y/n/q): ").strip().lower()

        if feed == 'y':
            dog.feed()
            print(f"{dog.name()} has been fed.")
        elif feed == 'q':
            break
