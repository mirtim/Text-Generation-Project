#
#   Final Project
#

import math

def clean_text(txt):
    """Fuction gets rid of all the punctuation in the text and makes it lower case"""
    for i in txt:
        t = [".", ",", "!", "?", '"', "-", ":", ";", "(", ")"]
        if i in t:
            txt = txt.replace(i, '')
    txt = txt.lower()
    return txt

def stem(s):
    suffixes = ["ing", "ed", "er", "ly", "able", "ible", "ment", "ness", "ism",
                "ist", "dom", "ship", "ize", "ful", "less", "ous", "ive"]
    if s[-3:] == "ing":
        if s[-4:] == s[-5:]:
            s = s[:-4]
        elif len(s[:-3]) < 2:
            s = s[:-3]
    elif "er" in s[-3:]:
        if s[-2:] == "er":
            s = s[:-2]
        else:
            s = s[:-3]
    elif s[-2:] == "ed":
        s = s[:-1]
    elif s[-2:] == "es":
        if s[-3:] == "i":
            s = s[:-3] + "y"
    elif s[-2:] == "ty":
        if s[-3:] == "i":
            s = s[:-3]
    elif s[-3:] == "ful":
        if s[-4:] == "i":
            s = s[:-4] + "y"
    elif s[-3:] == "ive":
        if s[-4:] == "s":
            s = s[:-3] + "e"
    elif s[-1:] == "y":
        s = s[:-1] + "i"
    else:
        for i in suffixes:
            if i in s[-4:]:
                s = s.replace(i, '')

    return s

def split_sentences(s):
    replaceTheseThings = (". ", "? ", "! ")
    for w in replaceTheseThings:
        s = s.replace(w, '@')
    sentences = s.split("@")
    return sentences

def compare_dictionaries(d1, d2):
    score = 0
    total = 0
    for i in d1:
        total += d1[i]
    for j in d2:
        if j in d1:
            prob = d1[j]/total
            score += math.log(prob)*d2[j]
        else:
            score += math.log(0.5/total)*d2[j]
    return round(score, 3)


class TextModel:

    def __init__(self, model_name):
        """class constructor"""
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.adjacent_words = {}

    def __repr__(self):
        """Return a string representation of the TextModel."""
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths:  ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of adjacent words: ' + str(len(self.adjacent_words)) + '\n'
        return s

    def add_string(self, s):
        """Analyzes the string txt and adds its pieces
        to all of the dictionaries in this text model.
        """
        sentences = split_sentences(s)
        lengths_list = []

        for i in sentences:
            count = 1
            for j in i:
                if j == " ":
                    count += 1
            lengths_list += [count]
        for x in lengths_list:
            if x in self.sentence_lengths:
                self.sentence_lengths[x] += 1
            else:
                self.sentence_lengths[x] = 1

        # Add code to clean the text and split it into a list of words.
        word_list = clean_text(s)
        word_list = word_list.split(" ")
        word_list = [x.replace(" ", "") for x in word_list]
        stem_list = [stem(x) for x in word_list]

        for i in stem_list:
            if i in self.stems:
                self.stems[i] += 1
            else:
                self.stems[i] = 1

        # Template for updating the words dictionary.
        for w in word_list:
            if w in self.words:
                self.words[w] += 1
            else:
                self.words[w] = 1

        # Add code to update other feature dictionaries.
        for q in word_list:
            if len(q) in self.word_lengths:
                self.word_lengths[len(q)] += 1
            else:
                self.word_lengths[len(q)] = 1

        for r in range(len(word_list)):
            if word_list[r] == word_list[-1]:
                r = r
            else:
                pair = word_list[r] + word_list[r+1]
                if pair in self.adjacent_words:
                    self.adjacent_words[pair] += 1
                else:
                    self.adjacent_words[pair] = 1




    def add_file(self, filename):
        """Function adds the file """
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        text = f.read()
        g = self.add_string(text)
        f.close()


    def save_model(self):
        """Function saves the dictionaries to the files"""
        a = self.name + "_" + "words"
        f = open(a, 'w')               # Open file for writing.
        f.write(str(self.words))       # Writes the dictionary to the file.
        f.close()

        b = self.name + "_" + "word_lengths"
        t = open(b, 'w')
        t.write(str(self.word_lengths))
        t.close()

        c = self.name + "_" + "stems"
        m = open(c, 'w')
        m.write(str(self.stems))
        m.close()

        d = self.name + "_" + "sentence_lengths"
        n = open(d, 'w')
        n.write(str(self.sentence_lengths))
        n.close()

        e = self.name + "_" + "adjacent_words"
        o = open(e, 'w')
        o.write(str(self.adjacent_words))
        o.close()

    def read_model(self):
        """Function opens the files and assigns the dictionaries"""
        a = open(self.name + "_" + "words", 'r')    # Open for reading.
        a_str = a.read()                  # Read in a string that represents a dict.
        a.close()

        self.words = dict(eval(a_str))      # Convert the string to a dictionary.

        b = open(self.name + "_" + "word_lengths", 'r')    # Open for reading.
        b_str = b.read()                  # Read in a string that represents a dict.
        b.close()

        self.word_lengths = dict(eval(b_str))

        c = open(self.name + "_" + "stems", 'r')
        c_str = c.read()
        c.close()

        self.stems = dict(eval(c_str))

        d = open(self.name + "_" + "sentence_lengths", 'r')
        d_str = d.read()
        d.close()

        self.sentence_lengths = dict(eval(d_str))

        e = open(self.name + "_" + "adjacent_words", 'r')
        e_str = e.read()
        d.close()

        self.adjacent_words = dict(eval(e_str))

    def similarity_scores(self, other):
        scores = []
        scores += [compare_dictionaries(other.words, self.words)]
        scores += [compare_dictionaries(other.word_lengths, self.word_lengths)]
        scores += [compare_dictionaries(other.stems, self.stems)]
        scores += [compare_dictionaries(other.sentence_lengths, self.sentence_lengths)]
        scores += [compare_dictionaries(other.adjacent_words, self.adjacent_words)]

        return scores

    def classify(self, source1, source2):

        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        print("scores for ", source1.name, ": ", scores1)
        print("scores for ", source2.name, ": ", scores2)
        count = 0
        for i in range(len(scores1)):
            if scores1[i] > scores2[i]:
                count += 1
        if count > len(scores1) // 2:
            print("mystery is more likely to have come from ", source1.name)
        else:
            print("mystery is more likely to have come from ", source2.name)






def test():

    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)

def run_tests():

    source1 = TextModel('harry1')
    source1.add_file('harry1.txt')

    source2 = TextModel('narnia')
    source2.add_file('narnia.txt')

    new1 = TextModel('harry2')
    new1.add_file('harry2.txt')
    new1.classify(source1, source2)
