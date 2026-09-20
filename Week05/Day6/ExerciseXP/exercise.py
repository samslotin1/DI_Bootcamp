# OOP Quiz Answers

## What is a class?

A class is a blueprint for creating objects. It defines the attributes and methods that its objects will have.

## What is an instance?

An instance is a specific object created from a class.

## What is encapsulation?

Encapsulation means keeping data and the methods that work on that data together inside a class. It also helps control access to the internal details of an object.

## What is abstraction?

Abstraction means hiding unnecessary implementation details and showing only the important features or behavior.

## What is inheritance?

Inheritance is when one class gets attributes and methods from another class. The class that inherits can reuse or extend the behavior of the parent class.

## What is multiple inheritance?

Multiple inheritance is when a class inherits from more than one parent class.

## What is polymorphism?

Polymorphism means that different classes can use the same method name, but each class can implement the method in its own way.

## What is method resolution order or MRO?

Method Resolution Order, or MRO, is the order Python follows when searching for a method or attribute in a class hierarchy, especially when inheritance or multiple inheritance is used.

  import random


class Card:
    suits = ("Hearts", "Diamonds", "Clubs", "Spades")
    values = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")

    def __init__(self, suit, value):
        if suit not in self.suits:
            raise ValueError(f"Invalid suit: {suit}")
        if value not in self.values:
            raise ValueError(f"Invalid value: {value}")

        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.value} of {self.suit}"


class Deck:
    def __init__(self):
        self.cards = []
        self.shuffle()

    def _create_full_deck(self):
        return [Card(suit, value) for suit in Card.suits for value in Card.values]

    def shuffle(self):
        self.cards = self._create_full_deck()
        random.shuffle(self.cards)

    def deal(self):
        if not self.cards:
            return None
        return self.cards.pop()


if __name__ == "__main__":
    deck = Deck()
    print(f"Cards in deck: {len(deck.cards)}")

    card = deck.deal()
    print(f"Dealt card: {card}")
    print(f"Cards left in deck: {len(deck.cards)}")
