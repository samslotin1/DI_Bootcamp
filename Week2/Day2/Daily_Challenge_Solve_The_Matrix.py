# Step 1

MATRIX_STR = '''
7ir
Tsi
h%x
i ?
sM# 
$a 
#t%'''

lines = MATRIX_STR.strip().splitlines()
matrix = []

for line in lines:
    matrix.append(list(line))

print(matrix)

# Step 2
decoded = ""

for col in range(len(matrix[0])):
    for row in range(len(matrix)):
        decoded += matrix[row][col]

print(decoded)

# Step 3

for ch in decoded:
    if ch.isalpha():
        pass
    else:
        pass

# Step 4
result = ""
in_symbol = False

for ch in decoded:
    if ch.isalpha():
        result += ch
        in_symbol = False
    else:
        if result and not in_symbol:
            result += " "
            in_symbol = True

# Step 5
print(result.strip())
