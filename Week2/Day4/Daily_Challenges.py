words = input("Give the words separated by commas: ")
word_list = words.split(",")
word_list.sort()
",".join(word_list)
result = ",".join(word_list)
print(result)

