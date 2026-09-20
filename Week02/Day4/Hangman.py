import random

wordslist = ['correction', 'childish', 'beach', 'python', 'assertive', 'interference', 'complete', 'share',
             'credit card', 'rush', 'south']
word = random.choice(wordslist)

hidden_word = []
for letter in word:
    hidden_word.append("*")

print(" ".join(hidden_word))

wrong_guesses = 0

while "*" in hidden_word:
    letter = input("Please enter a letter: ")

    if letter in word:
        for i in range(len(word)):
            if letter == word[i]:
                hidden_word[i] = letter
    else:
        wrong_guesses += 1
        print(f"Wrong! you have {6 - wrong_guesses} guesses left")

    if wrong_guesses == 6:
        print("You lose! The word was {word}")
        break
    print(" ".join(hidden_word))

else:
    print("You win!")
