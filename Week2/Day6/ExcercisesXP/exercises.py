# Exercise 1
class Cat:
    def __init__(self, cat_name, cat_age):
        self.name = cat_name
        self.age = cat_age

cat1 = Cat("Whiskers", 3)
cat2 = Cat("Davey", 1)
cat3 = Cat("Mama", 4)

def find_oldest_cat(cat1, cat2, cat3):
    oldest = cat1
    if cat2.age > oldest.age:
        oldest = cat2
    if cat3.age > oldest.age:
            oldest = cat3
    return oldest

oldest = find_oldest_cat(cat1, cat2, cat3)
print(f"The oldest cat is {oldest.name}, and is {oldest.age} years old.")

# Exercise 2
class Dog:
    def __init__(self, dog_name, dog_height):
        self.name = dog_name
        self.height = dog_height

    def bark(self):
        print(f"{self.name} goes woof!")

    def jump(self):
        print(f"{self.name} jumps {self.height * 2} cm high!")


davids_dog = Dog("Stinky", 50)
sarahs_dog = Dog("Sloopy", 20)

print(f"{davids_dog.name} is {davids_dog.height} cm tall")
print(f"{sarahs_dog.name} is {sarahs_dog.height} cm tall")

davids_dog.bark()
davids_dog.jump()
sarahs_dog.bark()
sarahs_dog.jump()

if davids_dog.height > sarahs_dog.height:
        print("David's dog is bigger than Sarah's dog!")
else:
        print("Sarah's dog is bigger than David's dog!")

# Exercise 3

class Song:
    def __init__(self, lyrics):
        self.lyrics = lyrics

    def sing_me_a_song(self):
        for line in self.lyrics:
            print(line)
stairway = Song(["There's a lady who's sure", "all that glitters is gold", "and she's buying a stairway to heaven"])

stairway.sing_me_a_song()

# Exercise 4

class Zoo:

    def __init__(self, zoo_name):
        self.zoo_name = zoo_name
        self.animals = []

    def add_animals(self, new_animal):
        if new_animal not in self.animals:
            self.animals.append(new_animal)

    def get_animals(self):
        for animal in self.animals:
            print(animal)

    def sell_animal(self, animal_sold):
        if animal_sold not in self.animals:
            print(f"{animal_sold} is not in the zoo.")
        else:
            self.animals.remove(animal_sold)

    def sort_animals(self):
        self.animals.sort()
        groups = {}

        for animal in self.animals:
            letter = animal[0]

            if letter in groups:
                groups[letter].append(animal)
            else:
                groups[letter] = [animal]

        self.groups = groups

    def get_groups(self):
        for letter, animals in self.groups.items():
            print(letter, ":", animals)


my_zoo = Zoo("Slotin Zoo")

my_zoo.add_animals("Ape")
my_zoo.add_animals("Baboon")
my_zoo.add_animals("Bear")
my_zoo.add_animals("Cat")
my_zoo.sort_animals()
my_zoo.get_groups()
