import glob
import json
import os
import random
import re
import string

from nltk import FreqDist, classify, NaiveBayesClassifier
from nltk.corpus import twitter_samples, stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize


def remove_noise(tweet_tokens, stop_words = ()):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens


def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token


def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)






if __name__ == "__main__":
    semantic_path = os.path.join(os.getcwd(), 'semantic')
    json_path = os.path.join(os.getcwd(), 'twitter/json_files')
    positive_tweets = twitter_samples.strings(os.path.join(semantic_path, 'positive_tweets.json'))
    negative_tweets = twitter_samples.strings(os.path.join(semantic_path, 'negative_tweets.json'))
    text = twitter_samples.strings(os.path.join(semantic_path, 'tweets.20150430-223406.json'))
    tweet_tokens = twitter_samples.tokenized(os.path.join(semantic_path, 'positive_tweets.json'))[0]

    stop_words = stopwords.words(os.path.join(semantic_path, 'english'))

    positive_tweet_tokens = twitter_samples.tokenized(os.path.join(semantic_path, 'positive_tweets.json'))
    negative_tweet_tokens = twitter_samples.tokenized(os.path.join(semantic_path, 'negative_tweets.json'))

    positive_cleaned_tokens_list = []
    negative_cleaned_tokens_list = []

    for tokens in positive_tweet_tokens:
        positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    for tokens in negative_tweet_tokens:
        negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    all_pos_words = get_all_words(positive_cleaned_tokens_list)

    freq_dist_pos = FreqDist(all_pos_words)
    print(freq_dist_pos.most_common(10))

    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

    positive_dataset = [(tweet_dict, "Positive")
                        for tweet_dict in positive_tokens_for_model]

    negative_dataset = [(tweet_dict, "Negative")
                        for tweet_dict in negative_tokens_for_model]

    dataset = positive_dataset + negative_dataset

    random.shuffle(dataset)

    train_data = dataset[:7000]
    test_data = dataset[7000:]

    classifier = NaiveBayesClassifier.train(train_data)

    print("Accuracy is:", classify.accuracy(classifier, test_data))

    print(classifier.show_most_informative_features(10))
    for f in glob.glob(json_path + "/*.json"):
        with open(f, "r") as read_file:
            data = json.load(read_file)

        positive_count = 0
        negative_count = 0
        total_count = 0
        vals = data.values()
        for v in vals:
            if v['text']:
                custom_tokens = remove_noise(word_tokenize(v['text']))
                semantic = classifier.classify(dict([token, True] for token in custom_tokens))
                #print(v['text'], semantic)
                total_count +=1
                if semantic== 'Positive':
                    positive_count += 1
                elif semantic == 'Negative':
                    negative_count +=1
        print(f)
        print("negative",negative_count)
        print("positive", positive_count)
        print("total", total_count)