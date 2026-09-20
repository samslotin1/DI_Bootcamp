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
