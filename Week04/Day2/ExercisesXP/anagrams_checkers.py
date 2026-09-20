lass AnagramChecker:
    def __init__(self):
        with open ("sowpods.txt", "r") as f:
               content = f.readlines()
        self.words = [w.strip() for w in content]

    def is_valid_word(self, word):
        if word in self.words:
            return True
        else:
            return False

    def is_anagram(self, word1, word2):
        if word1 == word2:
            return False
        if sorted(word1) == sorted(word2):
            return True
        else:
            return False

    def get_anagrams(self, word):
        anagrams = []
        for w in self.words:
            if self.is_anagram(word, w):
                anagrams.append(w)
        return anagrams

