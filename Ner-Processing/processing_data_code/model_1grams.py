import pandas as pd
import csv
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import TweetTokenizer
from preprocessingText import clean_text_special_characters


def oneGramModel(fileInput):
    tknzr = TweetTokenizer()
    data = pd.read_csv(fileInput, sep='\t', encoding='utf8', lineterminator='\n', usecols=[0], names=['text'],
                       low_memory=False, dtype=str)

    data["text"] = data["text"].astype(str)
    data["text"] = data["text"].apply(clean_text_special_characters)
    data['text'].dropna(inplace=True)

    for i, line in enumerate(data["text"]):
        data["text"][i] = ' '.join([x for x in tknzr.tokenize(str(line))])

    vectorizer = CountVectorizer(ngram_range=(1, 1)).fit(data["text"])

    bag_of_words = vectorizer.transform(data["text"])
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx])
                  for word, idx in vectorizer.vocabulary_.items()]
    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)

    with open(fileInput[:-4] + "-1gram.csv", "w", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerows(words_freq)


j = 0
while j < 65:
    file = "total_hydrated/extracted_tweets" + str(j) + '.csv'
    oneGramModel(file)
    print(j)
    j += 1
