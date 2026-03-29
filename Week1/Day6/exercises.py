# Exercise 1

keys = ['Ten', 'Twenty', 'Thirty']
values = [10, 20, 30]

for key, value in zip(keys, values):
    print(key, value)

# Exercise 2

family = {"rick": 43, 'beth': 13, 'morty': 5, 'summer': 8}

total = 0

for name, age in family.items():
    if age < 3:
        price = 0
    elif age <= 12:
        price = 10
    else:
        price = 15


    print(name, "pays", price)
    total = total + price

print("Total cost:", total)

# Exercise 3

brand = {
    "name": "Zara",
    "creation_date": 1975,
    "creator_name": "Amancio Ortega Gaona",
    "type_of_clothes": ["men", "women", "children", "home"],
    "international_competitors": ["Gap", "H&M", "Benetton"],
    "number_stores": 7000,
    "major_color": {
        "France": "blue",
        "Spain": "red",
        "US": ["pink", "green"]
    }
}

brand["number_stores"] = 2

print(brand["type_of_clothes"])

brand["country_creation"] = "Spain"

if "international_competitors" in brand:
    brand["international_competitors"].append("Desigual")

brand.pop("creation_date")

print(brand["international_competitors"][-1])

print(brand["major_color"]["US"])

print(len(brand))

print(brand.keys())

# Exercise 4


users = ["Mickey", "Minnie", "Donald", "Ariel", "Pluto"]

result = {}

for i, name in enumerate(users):
    result[name] = i

print(result)

# 2. index name

result ={}

for i, name in enumerate(users):
    result[i] = name

print(result)

# 3 sorted name index

result = {}

for i, name in enumerate(sorted(users)):
    result[name] = i

print(result)

