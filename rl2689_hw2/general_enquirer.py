__author__ = 'rogersjeffrey'
"""
  methods for processing the inquirer dictionary  and storing the negative and positive words
"""
import re
import csv
import pprint
import preprocessor
count=0
separator="|"
negative_words=[]
positive_words=[]
import cPickle as pickle
with open("general_inquiry_dictionary.txt","rb") as dev_data:
    for line in dev_data:
        if re.search(r'Negativ|Neg|Ngtv',line):
           negative_words.append(preprocessor.return_stemmed_word(line.split()[0].lower()))
            #print line.split()[0].strip()
        if re.search(r'Positiv|Pos',line):
           positive_words.append(preprocessor.return_stemmed_word(line.split()[0].lower()))
           #print line

pickle.dump(negative_words,open("negative_words.p","wb"))
pickle.dump(positive_words,open("positive_words.p","wb"))
