__author__ = 'rogersjeffrey'
import cPickle as pickle
from sys import  argv
(script_name,model_file)=argv
prior_word_conditional_prob_hash=pickle.load(open(model_file,"rb"))
prior_probabilities_hash=pickle.load(open("prior_class_probabilities.p","rb"))
feature_rank_hash=pickle.load(open("feature_ranks.p","rb"))
class0_features={}
class1_features={}
for words in feature_rank_hash:
    class0_features.update({words:feature_rank_hash[words]["0"]})
    class1_features.update({words:feature_rank_hash[words]["1"]})

class_0=[]
class_1=[]
for w in sorted(class0_features, key=class0_features.get, reverse=True):
  if class0_features[w] !=0.0:
      #print w, class0_features[w]
      class_0.append(w)
for w in sorted(class1_features, key=class1_features.get, reverse=True):
  if class1_features[w] !=0.0:
      #print w, class1_features[w]
      class_1.append(w)

feature_set=set(class_0+class_1)

count=0
top=15000
final_probability_hash={}
for word in feature_set:
    final_probability_hash.update({word:prior_word_conditional_prob_hash[word]})
    count=count+1
    if count==top:
       break
pickle.dump(final_probability_hash,open("prior_probabilities.p","wb"))
#print final_probability_hash