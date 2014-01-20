__author__ = 'rogersjeffrey'
import math
"""
This method  implements a naive bayes classifier that is used to clasify the  movie reviews based on
1) Prior Probabilities of Classes
2) Prior Probabilities of words
3)List of Positive words and negative words from the harvard inquirer

"""
def naive_bayes_classifier(prior_probabilities,prior_word_probabilities,word_tokens,positive_words,negative_words):

    class_0="0"
    class_1="1"

    # Prior Probabilities
    class_0_prior=prior_probabilities[class_0]
    class_1_prior=prior_probabilities[class_1]
    # Initialzing Prior Probabilities to Class Probabilites
    class_0_probability=class_0_prior
    class_1_probability=class_1_prior

    not_found=0
    pos_count=0
    neg_count=0
    length=len(word_tokens)
    for word in word_tokens:


      if word in positive_words:
         pos_count=pos_count+1
      if word in negative_words:
          neg_count=neg_count+1
      if word in ["girl","show" ,"studios"]:
         continue
      if  word in ["not","no" ]:
           if not_found ==1:
              not_found=0
           else:
                not_found=1

      else:
         not_found=0

      if not_found==1:
          word="not"+"_"+ word
      if word in prior_word_probabilities.keys():
         if class_0 in prior_word_probabilities[word].keys():
            class_0_probability=class_0_probability+prior_word_probabilities[word][class_0]
         if class_1 in prior_word_probabilities[word].keys():

            class_1_probability=class_1_probability+prior_word_probabilities[word][class_1]

    if class_0_probability > class_1_probability:
       return {"0":class_0_probability}
    else:
       return {"1":class_1_probability}

