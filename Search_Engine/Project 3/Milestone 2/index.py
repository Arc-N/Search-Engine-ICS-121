from nltk.tokenize import RegexpTokenizer
from collections import Counter
from bs4 import BeautifulSoup
import os
import pickle
import re

STOP_WORDS = ("www", "http", "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as",
              "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now")


class docInfo:
    def __init__(self, docID):
        self.docID = docID
        self.freq = 0
        self.idf = 0
        self.header = False


def createIndex():
    index = dict()
    for root, dirs, files in os.walk("./WEBPAGES_RAW"):
        print("Currently indexing: ", root, "\n")
        for name in files:
            document = os.path.join(root, name)
            with open(document, encoding="utf-8") as file:
                parsedText = BeautifulSoup(file.read(), "html.parser")
                tokenizer = RegexpTokenizer(r'\w+')

                # Body
                block = parsedText.find_all('body')
                tokens = []
                for b in block:
                    for token in tokenizer.tokenize(b.text):
                        if token not in STOP_WORDS:
                            tokens.append(token.lower())
                for t, f in Counter(tokens).items():
                    if t not in index:
                        index[t] = set()
                    docID = [str(x) for x in re.findall(r'\b\d+\b', document)]
                    documentID_Clean = docID[0] + '/' + docID[1]
                    temp = docInfo(documentID_Clean)
                    temp.freq = f
                    temp.idf = len(tokens)
                    temp.header = False
                    index[t].add(temp)

                # Header
                block = parsedText.find_all('h1,h2,h3')
                tokens = []
                for b in block:
                    for token in tokenizer.tokenize(b.text):
                        if token not in STOP_WORDS:
                            tokens.append(token.lower())
                for t, f in Counter(tokens).items():
                    if t not in index:
                        index[t] = set()
                    docID = [str(x) for x in re.findall(r'\b\d+\b', document)]
                    documentID_Clean = docID[0] + '/' + docID[1]
                    temp = docInfo(documentID_Clean)
                    temp.freq = f
                    temp.idf = len(tokens)
                    temp.header = True
                    index[t].add(temp)
    return index


if __name__ == '__main__':
    index = createIndex()
    with open(str('./invertedIndex.pickle'), 'wb') as file:
        pickle.dump(index, file)
        file.close()
