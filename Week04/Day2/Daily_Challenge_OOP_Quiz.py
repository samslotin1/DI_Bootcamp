# Part 1

# Class - a blueprint for creating objects, grouping attributes and methods together
# instance - specific object created by a class blueprint
# encapsulation - Keep data + the code uses it together, and control access
# abstraction - hide complexity, show only whats needed
# inheritence - Hiding internal details and showing only essential functionality.
# Multiple inheritence - A class inherits attributes and methods from another class.
# Polymorphism - Same method name behaves differently depending on the object.
# MRO (Method Resolution Order) - The order Python follows to find methods in a class hierarchy.


# Part 2
import random


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

class Deck:
    def __init__(self):
        suit = ["heart", "diamond", "club", "spade"]
        value = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        self.cards = []
        for suit in suit:
            for value in value:
                card = Card(suit, value)
                self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

deck = Deck()
deck.shuffle()
card = deck.deal()
print(card.suit)
print(card.value)
