# Challenge 1

word = input("Enter a word")

result = {}

for i, in letter enumerate(word):
    if letter in result:
        result[letter].append(i)
    else:
        result[letter] = [i]

print(result)

# Challenge 2

items_purchase = {"Water": "$1", "Bread": "$3", "TV": "$1,000", "Fertilizer": "$20"}
wallet = "$300"

items_purchase = {
    "Water": "$1",
    "Bread": "$3",
    "TV": "$1,000",
    "Fertilizer": "$20"
}

wallet = "$300"


wallet = int(wallet.replace("$", "").replace(",", ""))

basket = []

for item, price in items_purchase.items():

    clean_price = int(price.replace("$", "").replace(",", ""))

    if clean_price <= wallet:
        basket.append(item)
        wallet -= clean_price


if not basket:
    print("Nothing")
else:
    print(sorted(basket))
