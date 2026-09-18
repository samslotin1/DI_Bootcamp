"""Game logic for a command-line Rock, Paper, Scissors game."""

import random


class Game:
    """Play one round of Rock, Paper, Scissors."""

    ITEMS = ("rock", "paper", "scissors")

    def get_user_item(self):
        """Prompt until the player enters a valid item, then return it."""
        while True:
            item = input("Choose rock, paper, or scissors: ").strip().lower()
            if item in self.ITEMS:
                return item
            print("Invalid choice. Please enter rock, paper, or scissors.")

    def get_computer_item(self):
        """Choose and return a random item for the computer."""
        return random.choice(self.ITEMS)

    def get_game_result(self, user_item, computer_item):
        """Return 'win', 'draw', or 'loss' for the supplied items."""
        if user_item == computer_item:
            return "draw"

        winning_pairs = {
            ("rock", "scissors"),
            ("paper", "rock"),
            ("scissors", "paper"),
        }
        return "win" if (user_item, computer_item) in winning_pairs else "loss"

    def play(self):
        """Play one round, print its outcome, and return its result."""
        user_item = self.get_user_item()
        computer_item = self.get_computer_item()
        result = self.get_game_result(user_item, computer_item)

        messages = {
            "win": "You won!",
            "draw": "It's a draw!",
            "loss": "You lost.",
        }
        print(
            f"You selected {user_item}. The computer selected {computer_item}. "
            f"{messages[result]}"
        )
        return result

"""Command-line menu for Rock, Paper, Scissors."""

from game import Game


def get_user_menu_choice():
    """Display the menu and return a valid choice, or None for invalid input."""
    print("\nRock, Paper, Scissors")
    print("(p) Play a new game")
    print("(s) Show scores")
    print("(q) Quit")

    choice = input("Choose an option: ").strip().lower()
    if choice in {"p", "s", "q"}:
        return choice

    print("Invalid menu choice. Please enter p, s, or q.")
    return None


def print_results(results):
    """Print a friendly summary of all completed games."""
    print("\nGame summary")
    print(f"Wins:   {results['win']}")
    print(f"Losses: {results['loss']}")
    print(f"Draws:  {results['draw']}")
    print("Thanks for playing!")


def main():
    """Run the menu until the player quits."""
    results = {"win": 0, "loss": 0, "draw": 0}

    while True:
        choice = get_user_menu_choice()

        if choice == "p":
            result = Game().play()
            results[result] += 1
        elif choice == "s":
            print_results(results)
        elif choice == "q":
            print_results(results)
            break


if __name__ == "__main__":
    main()


