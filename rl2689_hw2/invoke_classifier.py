"""
This file is used to invoke the naive bayes classifier.
The script takes as input the  test file and outputs the prediction data
"""
__author__ = 'rogersjeffrey'
import cPickle as pickle
from sys import argv
import csv
import preprocessor
import naive_bayes_classifier as nb

(script_name,model_file,test_file)=argv
prior_word_conditional_prob_hash=pickle.load(open(model_file,"rb"))
feature_rank_hash=pickle.load(open("feature_ranks.p","rb"))
prior_probabilities=pickle.load(open("prior_class_probabilities.p","rb"))
count=-1
with open(test_file, 'rb') as csvfile:
     review_reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
     #review_reader.next()

     for row in review_reader:
         count=count+1
         if count==0:
            print "Id,Category"
            continue

         #rows=row[0].split(",",1)
         review_content=""
         #if len(rows)==2:
         #    review_content=rows[1]
         #elif len(rows)==1:
         #    review_content=rows[0]
         review_content=row[0]
         words=preprocessor.pre_process_sentence(review_content)
         negative_words=pickle.load(open("negative_words.p","rb"))
         positive_words=pickle.load(open("positive_words.p","rb"))
         class_data=nb.naive_bayes_classifier(prior_probabilities,prior_word_conditional_prob_hash,words,positive_words,negative_words )
         print str(count)+","+class_data.keys()[0]
         #print class_data.keys()[0]+","+review_content
         #break