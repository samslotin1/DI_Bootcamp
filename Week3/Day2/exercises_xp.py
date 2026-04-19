# Exercise 1
class Pets:
    def __init__(self,animals):
        self.animals = animals

    def walk(self):
        for animal in self.animals:
            animal.walk()

class Cat:
    def __init__(self,name, age):
        self.name = name
        self.age = age

    def walk(self):
        print(f"{self.name} is walking")

class Siamese(Cat):
    pass

class Bengal(Cat):
    pass

class Chartreux(Cat):
    pass

b1 = Bengal("Bob", 4)
c1 = Chartreux("Cathy", 5)
s1 = Siamese("Smith", 7)

all_cats = [b1,c1,s1]

sara_pets = Pets(all_cats)

sara_pets.walk()

# Exercise 2

class Dog:
    def __init__(self,name, age, weight):
        self.name = name
        self.age = age
        self.weight = weight

    def bark(self):
        return(f"{self.name} is barking")

    def run_speed(self):
        return self.weight / self.age * 10

    def fight(self, other_dog):
        my_power =self.run_speed() * self.weight
        other_power = other_dog.run_speed() * other_dog.weight
        if my_power > other_power:
            return(f"{self.name} Won")
        else:
            return(f"{self.name} Lost")

dog1 = Dog("Bob", 4, 5)
dog2 = Dog("Smith", 7, 6)
dog3 = Dog("Chartreux", 9, 8)

print(dog1.bark())
print(dog1.fight(dog2))

# Exercise 3
import random

class PetDog(Dog):
    def __init__(self,name,age,weight):
       super().__init__(name, age, weight)
       self.trained = False

    def train(self):
        print(self.bark())
        self.trained = True

    def play(self, *args):
        names = [dog.name for dog in args]
        print(f"{','.join(names)} all play together")

    def do_a_trick(self):
       if self.trained:
           tricks = ["does a barrel roll", "stands on his back legs", "shakes your hand", "plays dead"]
           print(f"{self.name} {random.choice(tricks)}")

pd1 = PetDog("Bob", 4, 5)
pd2 = PetDog("Rex", 3, 20)
pd3 = PetDog("Max", 5, 15)

pd1.train()
pd1.play(pd2, pd3)
pd1.do_a_trick()

# Exercise 4

class Person:
    def __init__(self,first_name, age,):
       self.first_name = first_name
       self.age = age
       self.last_name = ""

    def is_18(self):
        if self.age >= 18:
            return True
        else:
            return False
class Family:
    def __init__(self, last_name):
        self.last_name = last_name
        self.members = []

    def born(self, first_name, age):
        new_person = Person(first_name, age)
        new_person.last_name = self.last_name
        self.members.append(new_person)

    def check_majority(self, first_name):
        for person in self.members:
            if person.first_name == first_name:
                if person.is_18():
                    print("You are over 18, your parents Jane and John accept that you will go out with your friends")
                else:
                    print("Sorry, you are not allowed to go out with your friends.")

    def family_presentation(self):
        print(self.last_name)
        for person in self.members:
            print(person.first_name, person.age)

family = Family("Smith")
family.born("Jane", 25)
family.born("John", 15)
family.check_majority("Jane")
family.family_presentation()


