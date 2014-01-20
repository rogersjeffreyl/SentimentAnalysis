echo "Training the classifier......."
python train_naive_bayes.py $1 $2
echo "Selecting the features....."
python examine_word_counts.py $1

