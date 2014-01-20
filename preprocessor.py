__author__ = 'rogersjeffrey'
"""
   This file consists of the methods that  are used for preprocessing the training and the test data
"""
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import re
import time
from os import listdir
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

#Creates an instance of the porters stemmer
def porter_stemmer():
     stemmer=PorterStemmer()
     return stemmer


# Removes repeated characters  that occur in a word like "Loooooove to Love"
def remove_repeated_chars(word):
    repeat_regexp = re.compile(r'(\w*)(\w)\2(\w*)')
    repl = r'\1\2\3'
    if wordnet.synsets(word):
       return word
    repl_word = repeat_regexp.sub(repl, word)
    if repl_word != word:
       return remove_repeated_chars(repl_word)
    else:
        return repl_word


# replaces ca by cannot won't by will not e
def negation_replacer(word):
    replacement_patterns = [
                             (r'won\'t', 'will not'),
                             (r'wont', 'will not'),
                             (r'can\'t', 'cannot'),
                             (r'doesn\'t', 'does not'),
                             (r'cant', 'cannot'),
                             (r'i\'m', 'i am'),
                             (r'im', 'i am'),
                             (r'ain\'t', 'is not'),
                             (r'aint', 'is not'),
                             (r'(\w+)\'ll', '\g<1> will'),
                             (r'(\w+)n\'t', '\g<1> not'),
                             (r'(\w+)\'ve', '\g<1> have'),
                             (r'(\w+)\'s', '\g<1> is'),
                             (r'(\w+)\'re', '\g<1> are'),
                             (r'(\w+)\'d', '\g<1> would'),

                            ]
    patterns = [(re.compile(regex), repl) for (regex, repl) in replacement_patterns]
    for (pattern, repl) in patterns:
            (word, count) = re.subn(pattern, repl, word)
    return word

#returns the stemmed word for a given word using porters stemmer
def return_stemmed_word(word):
     stemmed_word= porter_stemmer().stem(word)
     if stemmed_word [ len(stemmed_word)-1] == "'":
        stemmed_word=stemmed_word[:len(stemmed_word)-1]
     return stemmed_word

# returns true if a word is a stop word
def return_is_stop_word(word):
  if word not in ["not", "no","cannot","but","yet"]:
    if word not in stopwords.words('english'):
       return False
    else:
       return True
# tokenizes a string  removing punctuations
# hypehnated words are preserved

def tokenize_string_without_punctuations(input_string):
    #tokenizer = RegexpTokenizer(r'(?<=)(?![0-9]+)(\w+[-]*(\w)*)')
    #tokenizer = RegexpTokenizer(r'(?<=)(?![0-9]+)(\w+)')
    tokenizer=RegexpTokenizer(r"(?<=)(?![0-9]+)[\w']+")
    return tokenizer.tokenize(input_string)

# Preprocessing module tokenizes a sentence without punctuations. It removes stop words, stems the words
# and replaces the occurences of characters repeated un-necessary in the words
def pre_process_sentence(sentence):
    sentence=negation_replacer(sentence)
    tokens=tokenize_string_without_punctuations(sentence)
    processed_words_list=[]
    for  each_token in tokens:
         if not return_is_stop_word(each_token):
            each_token=remove_repeated_chars(each_token)
            each_token=negation_replacer(each_token)
            final_processed_word=each_token
            final_processed_word=return_stemmed_word(final_processed_word)
            if return_is_stop_word(final_processed_word):
                continue
            processed_words_list.append(final_processed_word)
    return processed_words_list