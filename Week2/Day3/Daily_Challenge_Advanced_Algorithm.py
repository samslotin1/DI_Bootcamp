import random

list_of_numbers = [random.randint(0, 10000) for _ in range(20000)]

target_number   = 3728

seen = set()
pairs = []

for num in list_of_numbers:
    partner = target_number - num

    if partner in seen:
        pairs.append((num, partner))

    seen.add(num)

for pair in pairs:
    print(f"{pair[0]} and {pair[1]} sums to the target_number {target_number}")
