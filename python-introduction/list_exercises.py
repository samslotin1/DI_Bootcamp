# 1
numbers = [1, 2, 3, 4]
for number in numbers:
    print(number)

# 2
numbers = [1, 2, 3, 4]
for number in numbers:
    print(number * 20)

# 3
names = ["Elie", "Tim", "Matt"]
first_letters = []
for name in names:
    first_letters.append(name[0])
print(first_letters)

# 4
numbers = [1, 2, 3, 4, 5, 6]
evens = []
for number in numbers:
    if number % 2 == 0:
        evens.append(number)
print(evens)

# 5
list1 = [1, 2, 3, 4]
list2 = [3, 4, 5, 6]
common = []
for item in list1:
    if item in list2:
        common.append(item)
print(common)

# 6
words = ["Elie", "Tim", "Matt"]
reversed_words = []
for word in words:
    reversed_words.append(word[::-1].lower())
print(reversed_words)

# 7
string1 = "first"
string2 = "third"
letters = []
for letter in string1:
    if letter in string2:
        letters.append(letter)
print(letters)

# 8
divisible_by_12 = []
for number in range(1, 101):
    if number % 12 == 0:
        divisible_by_12.append(number)
print(divisible_by_12)

# 9
word = "amazing"
vowels = "aeiou"
no_vowels = []
for letter in word:
    if letter not in vowels:
        no_vowels.append(letter)
print(no_vowels)

# 10
list_of_lists = []
for _ in range(3):
    list_of_lists.append([0, 1, 2])
print(list_of_lists)

# 11
matrix = []
for _ in range(10):
    matrix.append([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
print(matrix)
