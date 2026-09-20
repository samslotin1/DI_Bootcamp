# Exercise 1

my_fav_numbers = {3, 7, 10}


my_fav_numbers.add(1)
my_fav_numbers.add(5)


my_fav_numbers.remove(5)


friend_fav_numbers = {2, 7, 8}


our_fav_numbers = my_fav_numbers.union(friend_fav_numbers)


print(our_fav_numbers)

# Exercise 2
numbers = (1,2,3)


 numbers = numbers + (4,)

 print(numbers)

 # Exercise 3

basket = ["Banana", "Apples", "Oranges", "Blueberries"]

basket.remove("Banana")
basket.remove("Blueberries")

basket.append("Kiwi")
basket.insert(0, "Apples")

print(basket.count("Apples"))

basket.clear()

print(basket)

# Exercise 4

numbers = []
current = 1.5

for i in range(8):
 if current.is_integer():
  numbers.append(int(current))
 else:
  numbers.append(current)

 current = current + 0.5

print(numbers)

# Exercise 5

for i in range(1, 21):
    print(i)

for i in range(1, 21):
    if i % 2 == 0:
        print(i)

# Exercise 6

while True:
    name = input("Enter your name: ")

    if name.isdigit() or len(name) < 3:
        print("Invalid input, try again")
    else:
        print("thank you")
        break

# Exercise 7

favorite_fruits = input("Enter your favorite fruits separated by spaces: ")
favorite_fruits = favorite_fruits.lower().split()

fruit = input("Enter the name of a fruit: ")
fruit = fruit.lower()

if fruit in favorite_fruits:
    print("You chose one of your favorite fruits! Enjoy!")
else:
    print("You chose a new fruit. I hope you enjoy it!")

# Exercise 8

toppings = []

while True:
    topping = input("Enter a pizza topping (or type 'quit' to finish): ")

    if topping.lower() == "quit":
        break

    print(f"Adding {topping} to your pizza.")
    toppings.append(topping)

print("Your toppings are:", toppings)

base_price = 10
total_price = base_price + (len(toppings) * 2.5)

print(f"Total cost: ${total_price}")

# Exercise 9

total_cost = 0

while True:
    age = input("Enter age (or type 'quit'): ")

    if age == "quit":
        break

    age = int(age)

    if age < 3:
        total_cost += 0
    elif age <= 12:
        total_cost += 10
    else:
        total_cost += 15

print("Total cost:", total_cost)
