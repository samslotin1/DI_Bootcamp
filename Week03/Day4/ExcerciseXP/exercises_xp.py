# Exercise 1
from multiprocessing.connection import address_type
from tkinter.font import nametofont


class Currency:
    def __init__(self, currency, amount):
        self.currency = currency
        self.amount = amount

    def __str__(self):
        return f"{self.amount} {self.currency}s"

    def __int__(self):
        return self.amount

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        if isinstance(other, int):
            return self.amount + other
        if isinstance(other, Currency):
            if self.currency == other.currency:
                return self.amount + other.amount
            raise TypeError(
                f"Cannot add between Currency type <{self.currency}> and <{other.currency}>"
            )

    def __iadd__(self, other):
        if isinstance(other, int):
            self.amount += other
            return self
        if isinstance(other, Currency):
            if self.currency == other.currency:
                self.amount += other.amount
                return self
            raise TypeError(
                f"Cannot add between Currency type <{self.currency}> and <{other.currency}>"
            )


c1 = Currency("dollar", 5)
c2 = Currency("dollar", 10)
c3 = Currency("shekel", 1)
c4 = Currency("shekel", 10)

print(c1)
print(int(c1))
print(repr(c1))
print(c1 + 5)
print(c1 + c2)
print(c1)
c1 += 5
print(c1)
c1 += c2
print(c1)

 # Exercise 3

import string
import random

x = string.ascii_lowercase
y = string.ascii_uppercase
letters = x + y

letters = random.choice(letters)

random_string = ""

for i in range(5):
    random_string += random.choice(letters)

print(random_string)

# Exercise 4

import datetime

today = datetime.datetime.now()

def get_current_date():
    today = datetime.datetime.now()
    print(today)

get_current_date()

# Exercise 5

import datetime
now = datetime.datetime.now()
print(now)

new_year = datetime.datetime(now.year + 1, 1, 1)
print(new_year)

time_left = new_year - now
print(time_left)

# Exercise 6

import datetime

now = datetime.datetime.now()
print(now)

birthdate = datetime.datetime.strptime("1992-11-12", "%Y-%m-%d")
print(birthdate)

time_lived = now - birthdate
print(time_lived)

# Exercise 7

from faker import Faker
fake = Faker()

users = []

def add_users(number):
    for i in range(number):
        user = {
            "name": fake.name(),
            "address": fake.address(),
            "language_code": fake.language_code(),
        }
        users.append(user)

add_users(5)
print(users)
