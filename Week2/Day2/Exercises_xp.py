# Exercise 1
def display_message():
    print("I am learning python")

display_message()

# Exercise 2

def favorite_book(title):
    print("One of my favorite books is", title)

favorite_book("1984")

# Exercise 3

def describe_city(city, country="Unknown"):
    print(city, "is in", country)

describe_city("Atlanta", "USA")
describe_city("Atlanta")

# Exercise 4

import random

def random_numbers(user_number):
    random_number = random.randint(1, 100)

    if user_number == random_number:
        print("You are right")
    else:
        print("You are wrong", user_number, random_number)

random_numbers(50)

# Exercise 5

def make_shirt(size="large", text="I love python"):
    print("The shirt is this size", size, "and says", text)


make_shirt()
make_shirt("medium")
make_shirt("small", "I love lamp")

# Exercise 6

magician_names = ['Harry Houdini', 'David Blaine', 'Criss Angel']

def show_magicians(names):
    for magician in names:
        print(magician)

def make_great(names):
    for i in range(len(names)):
        names[i] = names[i] + " the Great"

make_great(magician_names)
show_magicians(magician_names)

# Exercise 7

import random

def get_random_temp():
    return random.randint(-10, 40)

def main():
    temp = get_random_temp()
    print("The temperature right now is", temp, "degrees Celsius")

    if temp < 0:
        print("Brrr, that's freezing! Wear some extra layers today")

    elif temp >=0 and temp <= 16:
        print("Quite chilly! Don't forget your coat. ")
    elif temp >= 17 and temp <= 23:
        print("Nice weather.")
    elif temp >= 24 and temp <=32:
        print("A bit warm, stay hydrated.")
    elif temp >= 33 and temp <=40:
        print("It's really hot! Stay cool.")

main()
