class Text:
    def __init__(self, text):
        self.text = text

    def word_frequency(self, word):
        words = self.text.split()
        result = words.count(word)

        if result == 0:
            return ("word not found")
        else:
            return result

    def most_common_word(self):
        my_dict = {}

        for word in self.text.split():
            if word not in my_dict:
                my_dict[word] = 1
            else:
                my_dict[word] += 1

        most_common = max(my_dict, key=my_dict.get)
        return most_common

    def unique_words(self):
        words = self.text.split()
        unique = set(words)
        return list(unique)

    @classmethod
    def from_file(cls, file_path):
        with open(file_path, "r") as file:
            content = file.read()
        return cls(content)

