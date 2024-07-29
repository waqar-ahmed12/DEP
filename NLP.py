import pandas as pd

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')
stopWords = set(stopwords.words('english'))

df = pd.read_csv('./Reddit_Data.csv')
df = df.head(4000)
df.head()
def preprocess(text):
  tokens = word_tokenize(text)  # Tokenize the text
  filtered_tokens = [word for word in tokens if word.lower() not in stopWords and word.isalpha()]  # Remove stop words and non-alphabetic tokens
  return ' '.join(filtered_tokens)

text = "this is a word FKDJSAL&*(^jfkdlsa)"
preprocess(text)
# df['clean_comment'] = df['clean_comment'].astype(str).apply(lower)  # make all the text in lower case
df['clean_comment'] = df['clean_comment'].astype(str).apply(preprocess) # remove the punctuations
df.head()
def sentimentAnalyze(text):
    return SentimentIntensityAnalyzer().polarity_scores(text)
     
# df['clean_comment'][0]
df['sentiment'] = df['clean_comment'].astype(str).apply(sentimentAnalyze)

df
def test(text):
    score = sentimentAnalyze(text)
    compound = score['compound']

    if compound >= 0.05:
        print("Overall Sentiment: Positive")
    elif compound <= -0.05:
        print("Overall Sentiment: Negative")
    else:
        print("Overall Sentiment: Neutral")

test("I believe there should be more to my order. I am very disappointed.")
test("Very satisfied. I'll be ordering more.")
test("Bring me this relic now.")
