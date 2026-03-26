Exercise 1 : Dictionary

# 1
pairs = [("name", "Elie"), ("job", "Instructor")]
result = {}
for key, value in pairs:
    result[key] = value
print(result)

# 2
states = ["CA", "NJ", "RI"]
names = ["California", "New Jersey", "Rhode Island"]
state_dict = {}
for i in range(len(states)):
    state_dict[states[i]] = names[i]
print(state_dict)

# 3
vowels = "aeiou"
vowel_dict = {}
for vowel in vowels:
    vowel_dict[vowel] = 0
print(vowel_dict)

# 4
alphabet_dict = {}
for i in range(26):
    alphabet_dict[i + 1] = chr(65 + i)
print(alphabet_dict)
