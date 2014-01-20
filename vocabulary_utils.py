__author__ = 'rogersjeffrey'
"""
  This module is used to  read the train data and  construct information  like word counts, prior class probabilities

"""
import csv
import preprocessor
import nltk
class vocabulary_utils:

    def __init__(self,train_file):
        self.input_file=train_file
        self.vocabulary_hash={}
        self.class_counts_hash={}
        self.total_sentence_count=0
        self.words_per_class={}
        self.reviews_per_class={}
        self.reviews_per_word={}
        self.pos_list={}
        self.not_found=0


    # Method for  checking for POS tag
    # @deprecated as it decreased the accuracy

    def update_pos_tags(self,tokens):
        tag_token_pairs=nltk.pos_tag(tokens)
        count=-1
        for word in tokens:
            count+=1
            if word in self.pos_list.keys():
               tokens_list=self.pos_list[word]
               if tag_token_pairs[count][1] in tokens_list:
                  continue
               else:
                   tokens_list=tag_token_pairs[count][1]
                   self.pos_list[word]=tokens_list
            else:
                tokens_list=tag_token_pairs[count][1]
                self.pos_list.update({word:tokens_list})

    # Assigning reviews ids to each review to be used for later processing
    def update_review_number_for_review_type(self,review_type):
        if review_type in self.reviews_per_class:
           reviews=self.reviews_per_class[review_type]
           reviews.append("R"+str(self.total_sentence_count))
           self.reviews_per_class[review_type]=reviews
        else:
           self.reviews_per_class.update({review_type:["R"+str(self.total_sentence_count)]})

    #TO find the count  of the reviews
    def update_review_list_for_word(self,word):
        review_id="R"+str(self.total_sentence_count)
        if word in self.reviews_per_word.keys():

           if review_id not in self.reviews_per_word[word]:
              reviews=self.reviews_per_word[word]
              reviews.append(review_id)
              self.reviews_per_word[word]=reviews
        else:
           self.reviews_per_word.update({word:[review_id]})


    # Read the train data file and get the count of words
    def get_vocab_counts_from_csv(self):

        review_count=0
        with open(self.input_file, 'rb') as csvfile:
            review_reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
            review_reader.next()
            for row in review_reader:


                rows=row[0].split(",",1)
                review_type=rows[0]
                review_content=rows[1]
                #print review_content
                self.total_sentence_count=self.total_sentence_count+1
                review_type=str(review_type)
                #Organizing the reviews based on the review type
                self.update_review_number_for_review_type(review_type)

                #updating the class counts
                if review_type in self.class_counts_hash.keys():
                   class_count=self.class_counts_hash[review_type]
                   class_count=class_count+1
                   self.class_counts_hash[review_type]=class_count
                else:
                   self.class_counts_hash.update({review_type:1})

                #@depricated POS tagging
                #pos_tagging_tokens=preprocessor.tokenize_string_without_punctuations(review_content)
                #self.update_pos_tags(pos_tagging_tokens)
                final_tokens=preprocessor.pre_process_sentence(review_content)
                self.construct_vocabulary_hash(review_type,final_tokens)

        csvfile.close()
        #pprint.pprint(self.vocabulary_hash)

    def construct_vocabulary_hash(self,review_type,pos_tagging_tokens):


        #Updating the word count for  each class
        not_found=0

        for each_word in pos_tagging_tokens:

            other_review_type=str(0)
            word=each_word
            if review_type==str(0):

                  other_review_type=str(1)
            else:
                  other_review_type=str(0)
            # if not occurs append not after every word found till End of Line
            if  each_word =="not":

                if not_found ==1:
                    not_found=0
                else:
                    not_found=1

            if not_found==1:
               each_word="not"+"_"+each_word


            self.update_review_list_for_word(each_word)
            if review_type in self.words_per_class.keys():
               total_word_in_class=self.words_per_class[review_type]
               self.words_per_class[review_type]=total_word_in_class+1
            else:
               self.words_per_class.update({review_type:1})


            if each_word in self.vocabulary_hash.keys():
               word_in_class_hash=self.vocabulary_hash[each_word]
               if review_type in word_in_class_hash:
                  count=self.vocabulary_hash[each_word][review_type]
                  self.vocabulary_hash[each_word][review_type]=count+1

               else:
                  self.vocabulary_hash[each_word][review_type]=1
            else:
               self.vocabulary_hash.update({each_word:{review_type:1}})

            not_found=0
            if not_found==1:
               each_word=word
               review_type=other_review_type
               self.update_review_list_for_word(each_word)
               if each_word in self.vocabulary_hash.keys():
                  word_in_class_hash=self.vocabulary_hash[each_word]
                  if review_type in word_in_class_hash:
                     count=self.vocabulary_hash[each_word][review_type]
                     self.vocabulary_hash[each_word][review_type]=count+1

                  else:
                    self.vocabulary_hash[each_word][review_type]=1
               else:
                  self.vocabulary_hash.update({each_word:{review_type:1}})



