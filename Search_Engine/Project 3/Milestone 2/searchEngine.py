from index import docInfo
from index import STOP_WORDS
from nltk.tokenize import RegexpTokenizer
from bs4 import BeautifulSoup
import json
import math
import pickle


def search(searchTerm):
    invertedIndex = 0
    with open('./invertedIndex.pickle', 'rb') as file:
        invertedIndex = pickle.load(file)
        file.close()
    # print(len(invertedIndex))
    searchTerms = searchTerm.split()
    ranking = dict()
    for term in searchTerms:
        if term not in STOP_WORDS:
            if not (term in invertedIndex):
                print("Couldn't find relevant information with that query...\n")
                continue
            for d in invertedIndex[term]:
                docID = d.docID
                tf_idf = 1+d.freq/d.idf
                if(d.header):
                    tf_idf += tf_idf*0.1
                if docID in ranking:
                    ranking[docID] += tf_idf
                else:
                    ranking[docID] = tf_idf

    ranking = sorted(ranking.items(), key=lambda x: (-x[1], x[0]))
    URLs = []

    with open('C:/Users/arake/Desktop/Search_Engine/WEBPAGES_RAW/bookkeeping.json') as json_data:
        js = json.load(json_data)
        for (key, value) in ranking:
            URLs.append(js[key])
    print("Found Total of: ", len(URLs), " URLs\n")
    for url in URLs[:20]:
        print(url)


if __name__ == "__main__":
    query = input('Search Query : ')
    search(str(query).lower())
