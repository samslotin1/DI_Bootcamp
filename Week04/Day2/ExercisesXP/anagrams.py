from anagram_checker import AnagramChecker

while True:
    print("1. Enter a word")
    print("2. Exit")
    choice = input("choose an option: ")
    if choice == "2":
        break
    elif choice == "1":
        print("Enter a word")
        word = input("enter a word: ").strip().upper()
        if len(word.split()) > 1:
            print("Error: please enter a single word")
        elif not word.isalpha():
            print("Error: only alphabetic characters are allowed")
        else:
            checker = AnagramChecker()
            is_valid = checker.is_valid_word(word)
            anagrams = checker.get_anagrams(word)
            if is_valid:
                print("YOUR WORD: " + word + " is a valid English word")
            else:
                print("YOUR WORD: " + word + " is not a valid English word")
            print("Anagrams: " + ", ".join(anagrams))
