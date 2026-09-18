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
