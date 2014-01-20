__author__ = 'rogersjeffrey'
import math
import pprint
# review dictionary- contains list of documents categorized per review class
# list of reviews for word- has all the reviewsin which the word appears irrespecive of the class
#Calcualtes the score of features based  on mutual information
def calculate_feature_score(review_dict,list_of_reviews_for_word,review_type ):

    #All documents for a particular review type
    documents_for_review_class=""
    #   pprint.pprint(review_dict)
    try:
      documents_for_review_class=review_dict[review_type]
    except KeyError:
      documents_for_review_class=""

    other_class_type=str(0)
    # Finding the complimentary class. since there are ony two classes
    if review_type==str(0):
       other_class_type=str(1)
    elif review_type==str(1):
       other_class_type=str(0)

    word_review_list=set(list_of_reviews_for_word)
    try:
      documents_in_other_review_class=review_dict[other_class_type]
    except KeyError:

      documents_in_other_review_class=""

    doc_in_rev_class_set=set(documents_for_review_class)
    doc_not_in_rev_class_set=set(documents_in_other_review_class)
    S01=doc_in_rev_class_set.difference(word_review_list)
    N01=len(S01)
    S11=doc_in_rev_class_set.intersection(word_review_list)
    N11=len(S11)
    S10=doc_not_in_rev_class_set.intersection(word_review_list)
    N10=len(S10)

    S=doc_in_rev_class_set.union(doc_not_in_rev_class_set)
    N=len(S)
    S00=doc_not_in_rev_class_set.difference(word_review_list)
    N00=len(S00)

    N1X=N10+N11
    NX1=N01+N11
    N0X=N01+N00
    NX0=N00+N10


    a1=0.0
    b1=0.0
    c1=0.0
    d1=0.0
    if N00!=0.0:
       a1=(float(N00)/float(N))*math.log((float(N*N00)/float(N0X*NX0)),2)
    if N01!=0.0:
       b1=(float(N01)/float(N))* math.log(float((N*N01)/float(N0X*NX1)),2)
    if N10!=0.0:
       c1=(float(N10)/float(N))* math.log((float(N*N10)/float(N1X*NX0)),2)
    if N11!=0.0:
       d1=(float(N11)/float(N))* math.log(float((N*N11)/float(N1X*NX1)),2)


    #print a1,b1,c1,d1
    MI=a1+b1+c1+d1
    return MI