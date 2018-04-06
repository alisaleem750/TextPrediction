import re
from collections import Counter
import logging as logger

class Ngrams:

    def __init__(self):
        # Using regex to exclude punctuation when converting from sentence to list.
        self.input_list = []
        self.bigrams = {}
        self.trigrams = {}
        self.counter = {}
        self.sortedCounter = ()

    # This method will return the list that is to be converted into Ngrams.
    def get_list(self):
        return self.input_list

    # This method will split the text into words that are put in a list to be converted into Ngrams.
    def set_list(self, text):
        self.input_list = re.findall("(\w+[\w'\-&]*)", text.upper())

    # def test_list(self):
    #     text = "We will have we will not we wish we could we wish we could we want we could"
    #     self.set_list(text)

    # This method will use the input list to convert the items in the list into bi-grams.
    def find_bigrams(self, input_list):
        self.load_bigrams()
        self.bigrams = self.add_ngrams(self.bigrams, input_list, 2)
        self.save_bigrams()
        return self.bigrams

    # This method will use the input list to convert the items in the list into tri-grams.
    def find_trigrams(self, input_list):
        self.load_trigrams()
        self.trigrams = self.add_ngrams(self.trigrams, input_list, 3)
        self.save_trigrams()
        return self.trigrams

    # This method puts the words in the input list into n-grams. Input list is the list based on which the n-grams will
    # be generated and n is the number of grams used. i.e if n = 2, we will generate bi-grams.
    def add_ngrams(self, ngramList, input_list, n):
        ngrams = ngramList
        length = len(input_list)
        for i in range(0, length - (n - 1)):
            if n > 2:
                ngramInput = ""
                for j in range(0, n - 1):
                    if j < n - 2:
                        ngramInput += input_list[i + j] + " "
                    else:
                        ngramInput += input_list[i + j]
                if ngramInput not in ngrams:
                    ngrams[ngramInput] = []
                ngrams[ngramInput].append(input_list[i + (n - 1)])
            else:
                if input_list[i] not in ngrams:
                    ngrams[input_list[i]] = []
                ngrams[input_list[i]].append(input_list[i + 1])
        return ngrams

    # This method returns the bi-grams.
    def get_bigrams(self):
        return self.bigrams

    # This method sets the bi-grams to the bi-grams given as input.
    def set_bigrams(self, bigrams):
        self.bigrams = bigrams

    # This method gets the tri-grams.
    def get_trigrams(self):
        return self.trigrams

    # This method sets the tri-grams to the tri-grams given as input.
    def set_trigrams(self, trigrams):
        self.trigrams = trigrams

    # This method will write the bi-grams to a bigrams.txt file.
    def save_bigrams(self):
        with open('../Ngrams/bigrams.txt', 'w') as bigrams:
            bigrams.write(str(self.bigrams))

    # This method will load the bi-grams from the bigrams.txt file.
    def load_bigrams(self):
        with open('../Ngrams/bigrams.txt', 'r') as bigrams:
            self.bigrams = eval(bigrams.read())
        return self.bigrams

    # This method will write the tri-grams to a trigrams.txt file.
    def save_trigrams(self):
        with open('../Ngrams/trigrams.txt', 'w') as trigrams:
            trigrams.write(str(self.trigrams))


    # This method will load the tri-grams from the trigrams.txt file.
    def load_trigrams(self):
        with open('../Ngrams/trigrams.txt', 'r') as trigrams:
            self.trigrams = eval(trigrams.read())
        return self.trigrams

    # Use python counter to count n-gram occurrences in list of words following the given words.
    def counter_ngrams(self, nGramDict, word):
        if nGramDict.has_key(word.upper()):
            self.counter = Counter(nGramDict[word.upper()])
        else:
            nGramDict[word] = []

    # Here, the frequency is set by the value of the result of the above CounterNgrams method.
    def sort_ngrams_by_frequency(self, nGramDict, word):
        self.counter_ngrams(nGramDict, word)
        if self.counter:
            self.sortedCounter = sorted(self.counter.items(), key=lambda x: x[1], reverse=True)
            return self.sortedCounter
        else:
            nGramDict[word] = []

    # This will show us the N most common n grams and their count in descending order (from most common to least)
    def top_n_common_ngrams(self, nGramDict, word):
        self.sort_ngrams_by_frequency(nGramDict, word)
        return self.sortedCounter

    # This method will return the top N words that start with the specified characters in the parameters. The list given
    # will be from most common to least common N words.
    def top_n_words_starting_with_characters(self, nGramDict, word, n, characters):
        self.top_n_common_ngrams(nGramDict, word)
        if self.sortedCounter:
            m = n
            while m > 0:
                worldList = []
                for word in self.sortedCounter:
                    if word[0].startswith(characters.upper()):
                        worldList.append(word[0])
                        m -= 1
                m = 0
            return worldList[:n]
        else:
            return ""

    # This will help us predict the first word of a sentence as the user types it by matching the characters typed with
    # the keys in the provided dictionary (bi-grams for our use-case). The N represents the amount of keys (predictions)
    # that are to be returned to the user.
    def return_keys_containing_characters(self, nGramDict, characters, n):
        keylist = []
        for key in nGramDict.keys():
            if key.startswith(characters.upper()):
                keylist.append(key)
        return keylist[:n]
