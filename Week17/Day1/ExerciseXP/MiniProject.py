from pathlib import Path


class AnagramChecker:
    def __init__(self, word_list_path="sowpods.txt"):
        path = Path(word_list_path)
        if not path.is_absolute():
            path = Path(__file__).parent / path

        with path.open("r", encoding="utf-8") as file:
            self.words = {line.strip().upper() for line in file if line.strip()}

    def is_valid_word(self, word):
        return word.upper() in self.words

    def is_anagram(self, word1, word2):
        word1 = word1.upper()
        word2 = word2.upper()
        return word1 != word2 and sorted(word1) == sorted(word2)

    def get_anagrams(self, word):
        word = word.upper()
        return sorted(
            candidate.lower()
            for candidate in self.words
            if self.is_anagram(word, candidate)
        )



from anagram_checker import AnagramChecker


def show_menu():
    print("\nAnagram Checker")
    print("1. Enter a word")
    print("2. Exit")
    return input("Choose an option: ").strip()


def get_valid_user_word():
    user_input = input("Enter a word: ").strip()

    if len(user_input.split()) != 1:
        print("Error: Please enter only one word.")
        return None

    if not user_input.isalpha():
        print("Error: Please use alphabetic characters only.")
        return None

    return user_input


def display_word_result(word, checker):
    word_upper = word.upper()

    print(f'\nYOUR WORD: "{word_upper}"')

    if not checker.is_valid_word(word):
        print("This is not a valid English word.")
        return

    anagrams = checker.get_anagrams(word)

    print("This is a valid English word.")
    if anagrams:
        print(f"Anagrams for your word: {', '.join(anagrams)}.")
    else:
        print("No anagrams were found for your word.")


def main():
    checker = AnagramChecker()

    while True:
        choice = show_menu()

        if choice == "1":
            word = get_valid_user_word()
            if word is not None:
                display_word_result(word, checker)
        elif choice == "2":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please choose 1 or 2.")


if __name__ == "__main__":
    main()
