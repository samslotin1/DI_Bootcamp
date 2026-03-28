# Exercise 1: Hello World
print(("Hello world\n") * 4)


# Exercise 2: Some Math
result = 99 ** 3 * 8
print(result)


# Exercise 3: What is the output?

# 5 < 3
# Guess: False
print(5 < 3)

# 3 == 3
# Guess: True
print(3 == 3)

# 3 == "3"
# Guess: False
print(3 == "3")

# "3" > 3
# Guess: Error → FIXED (converted type)
print(int("3") > 3)

# "Hello" == "hello"
# Guess: False
print("Hello" == "hello")


# Exercise 4: Your computer brand
computer_brand = "HP"
print(f"I have a {computer_brand} computer.")


# Exercise 5: Your information
name = "Sam"
age = 32
shoe_size = 10

info = f"My name is {name}, I am {age} years old and my shoe size is {shoe_size}."
print(info)


# Exercise 6: A & B
a = 2
b = 1

if a > b:
    print("Hello World")


# Exercise 7: Odd or Even
number = int(input("Enter a number: "))

if number % 2 == 0:
    print("Even")
else:
    print("Odd")


# Exercise 8: What's your name?
my_name = "Sam"
user_name = input("What is your name? ")

if user_name.lower() == my_name.lower():
    print("Same name. Nice.")
else:
    print("Different name. Cool.")


# Exercise 9: Tall enough to ride a roller coaster
height = int(input("Enter your height in cm: "))

if height >= 145:
    print("Access Granted")
else:
    print("Access Denied")
