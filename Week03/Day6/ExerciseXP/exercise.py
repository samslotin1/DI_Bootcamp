import json
import random
from pathlib import Path


WORDS_FILE = Path(__file__).with_name("words.txt")
OUTPUT_FILE = Path(__file__).with_name("modified_employee.json")


def get_words_from_file(file_path):
    """Read words from a file and return them as a list."""
    with open(file_path, "r") as file:
        content = file.read()

    return content.split()


def get_random_sentence(length):
    """Generate a random lowercase sentence with the requested number of words."""
    words = get_words_from_file(WORDS_FILE)
    random_words = []

    for _ in range(length):
        random_words.append(random.choice(words))

    sentence = " ".join(random_words)
    return sentence.lower()


def save_modified_json():
    """Access salary, add birth_date, and save the modified JSON to a file."""
    sampleJson = """{
       "company":{
          "employee":{
             "name":"emma",
             "payable":{
                "salary":7000,
                "bonus":800
             }
          }
       }
    }"""

    data = json.loads(sampleJson)
    salary = data["company"]["employee"]["payable"]["salary"]
    print(f"Salary: {salary}")

    data["company"]["employee"]["birth_date"] = "1995-04-17"

    with open(OUTPUT_FILE, "w") as file:
        json.dump(data, file, indent=4)

    print(f"Modified JSON saved to {OUTPUT_FILE.name}")


def main():
    print("This program creates a random sentence from a word list.")

    try:
        length = int(input("How long should the sentence be? Choose a number from 2 to 20: "))
    except ValueError:
        print("Error: Please enter a whole number.")
        return

    if length < 2 or length > 20:
        print("Error: The sentence length must be between 2 and 20.")
        return

    sentence = get_random_sentence(length)
    print(sentence)

    save_modified_json()


if __name__ == "__main__":
    main()
