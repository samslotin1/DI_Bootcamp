# Exercise 1: Hello World
# Print the following output using one line of code:
print(("Hello world\n") * 4)

# Exercise 2: Some Math
# Write code that calculates the result of:
result = 99 ** 3 * 8
print(result)

# Exercise 3: What is the output?
# Predict the output of the following code snippets.
# Comment what your guess is, then run the code and compare.
# Exercise 3: What is the output?
# Predict the output and comment your guess.

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
# Guess: Error
print("3" > 3)

# "Hello" == "hello"
# Guess: False
print("Hello" == "hello")

# Exercise 4: Your computer brand
# Create a variable called computer_brand which value is the brand name of your computer.
# Using the computer_brand variable, print a sentence that states:
# "I have a <computer_brand> computer."

computer_brand = "HP"
print("I have a " + computer_brand + " computer.")

# Exercise 5: Your information
# Create variables called name, age, and shoe_size.
# Create a variable called info that contains a sentence
# using the variables above.
# Print the info message.

name = "Sam"
age = 32
shoe_size = 10

info = "My name is " + name + ", I am " + str(age) + " years old and my shoe size is " + str(shoe_size) + "."

print(info)

# Exercise 6: A & B
# Create two variables, a and b.
# If a is bigger than b, print "Hello World".

a = 2
b = 1

if a > b:
    print("Hello World")

# Exercise 7: Odd or Even
# Ask the user for a number and determine if it is odd or even.

number = int(input("Enter a number: "))

if number % 2 == 0:
    print("Even")
else:
    print("Odd")

# Exercise 8: What's your name?
# Ask the user for their name and determine whether
# or not you have the same name.
# Print a funny message based on the outcome.

my_name = "Sam"

user_name = input("What is your name? ")

if user_name == my_name:
    print("Same name. Nice.")
else:
    print("Different name. Cool.")

# Exercise 9: Tall enough to ride a roller coaster
# Ask the user for their height in centimeters.
# If they are over 145 cm, print they are tall enough to ride.
# Otherwise, print they need to grow more.

height = int(input("Enter your height in cm: "))

if height > 145:
    print("Access Granted")
else:
    print("Access Denied")