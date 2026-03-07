import random

def number_guessing_game():
    random_number = random.randint(1, 100)
    max_attempts = 7

    for attempt in range(max_attempts):
        guess = int(input("Enter your guess (1-100): "))

        if guess < random_number:
            print("Too low!")
        elif guess > random_number:
            print("Too high!")
        else:
            print("Congratulations! You guessed the number!")
            break
    else:
        print("Sorry, you ran out of attempts.")
        print("The correct number was:", random_number)

number_guessing_game()