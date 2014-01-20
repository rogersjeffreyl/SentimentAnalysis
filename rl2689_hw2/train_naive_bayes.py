__author__ = 'rogersjeffrey'
"""
  This file contains methods that are used to train the naive bayes classifier.
  The trained parameters are then stored in a pickle file.
"""
import pickle
import pprint
import vocabulary_utils
from sys import  argv
import math
import feature_ranker


# Calculates  the prior class probabilities
def calculate_prior_probabilities(class_count,total_count):
    prob=0.0
    log_prob=0.0
    prob=float(class_count)/float(total_count)
    log_prob=math.log(prob,2)
    return log_prob

# calculates the prior word probabilities
# Laplace smoothing is applied to  calculate the probabilities
def calculate_word_conditional_probabilities(count_in_class,total_vocab_length,length_of_vocab_in_class):
    prob=0.0
    log_prob=0.0
    prob=(float(count_in_class)+1)/(float(total_vocab_length)+float(length_of_vocab_in_class))
    log_prob=math.log(prob,2)
    return log_prob

# Ranks the features based on a score
def compute_feature_score(review_dictionary,word_review_dictionary,review_type):
    return feature_ranker.calculate_feature_score(review_dictionary,word_review_dictionary,review_type)

# trains a naive bayes classifier based on the prior class probabilities and the word priors
def train_naive_bayes(training_file):
    vc_instance= vocabulary_utils.vocabulary_utils(training_file)
    vc_instance.get_vocab_counts_from_csv()

    #Prior probabilities estimation for classes

    prior_probabilities_hash={}

    for each_class  in vc_instance.class_counts_hash:

        prior_probabilities_hash.update({each_class:calculate_prior_probabilities(vc_instance.class_counts_hash[each_class],vc_instance.total_sentence_count)})


    prior_word_conditional_prob_hash={}
    feature_rank_hash={}
    previous_word=""
    same_word=False
    words_in_vocabulary=len(vc_instance.vocabulary_hash.keys())
    # Calculate the prior word probabilities for each class
    for each_word in vc_instance.vocabulary_hash.keys():
        for each_class in vc_instance.class_counts_hash:
            count_of_word_in_class=0
            each_class=str(each_class)
            if each_class not in vc_instance.vocabulary_hash[each_word]:
               count_of_word_in_class=0
            else:
                count_of_word_in_class=vc_instance.vocabulary_hash[each_word][str(each_class)]
            total_words_in_class=vc_instance.words_per_class[str(each_class)]
            score=compute_feature_score(vc_instance.reviews_per_class,vc_instance.reviews_per_word[each_word],str(each_class))

            if each_word in feature_rank_hash:
               if str(each_class) in feature_rank_hash[each_word]:
                  feature_rank_hash[each_word][each_class]=score
               else:
                 feature_rank_hash[each_word][each_class]={}
                 feature_rank_hash[each_word][each_class]=score
            else:

               feature_rank_hash.update({each_word:{each_class:score}})

            if each_word in prior_word_conditional_prob_hash.keys():
               word_hash=prior_word_conditional_prob_hash[each_word]
               if each_class not in word_hash.keys():
                  prior_word_conditional_prob_hash[each_word][str(each_class)]={}
                  prior_word_conditional_prob_hash[each_word][str(each_class)]=calculate_word_conditional_probabilities(count_of_word_in_class,words_in_vocabulary,total_words_in_class)
            else:
               probability=calculate_word_conditional_probabilities(count_of_word_in_class,words_in_vocabulary,total_words_in_class)
               prior_word_conditional_prob_hash.update({each_word:{str(each_class):probability}})

    #Serializing the prior probabilities hash
    pickle.dump(prior_word_conditional_prob_hash,open(model_file,"wb"))
    pickle.dump(feature_rank_hash,open("feature_ranks.p","wb"))
    pickle.dump(prior_probabilities_hash,open("prior_class_probabilities.p","wb"))
    pickle.dump(vc_instance.vocabulary_hash,open("vocabulary.p","wb"))

(script_name,model_file,csv_file_name)=argv
train_naive_bayes(csv_file_name)


