import re
import pandas as pd
import string
from collections import defaultdict
import math
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score

# Import dataset, spam ham data from Kaggle
data = pd.read_csv("emails.csv")

data.head()
# Preprocessing
def process(text):
    processed = re.sub(r'\b\w{1,2}\b', '', text)  # removed all one and two lettered words
    processed = re.sub(r'\s+', ' ', processed)  # replaced all whitespaces with one space
    processed = processed.translate(str.maketrans('', '', string.punctuation))  # removing all the punctuations
    return processed.lower().strip()  # converted to lower case and removed starting and ending spaces

def tokenize(list, resultList):
    for sentences in list:
        resultList.append(sentences.split())
    return resultList
numberOfSpams = data[data['spam'] == 1]
totalSpams = numberOfSpams.shape[0]
totalRows = data.shape[0]

totalHams = totalRows - totalSpams

probSpam = totalSpams / totalRows
probHam = totalHams / totalRows

probHam, probSpam

data['processedTexts'] = data['text'].apply(process)

# Splitting the data into training and test sets
trainData, testData = train_test_split(data, test_size=0.2, random_state=42)

# Extracting spam from ham, and tokenizing the words
spam = trainData[trainData['spam'] == 1]['processedTexts'].tolist()
ham = trainData[trainData['spam'] == 0]['processedTexts'].tolist()


spamSentences = []
hamSentences = []

# Separating each and every word, that is tokenizing it
tokenize(spam, spamSentences)
tokenize(ham, hamSentences)
# Define function to count what type of words are in spam and ham
def wordFrequencies(list):
    frequency = defaultdict(int)  # makes a dictionary with default value 0
    for sentences in list:
        for words in sentences:
            frequency[words] += 1  # if we find a word, increment it by 1
    return frequency

spamWordsFrequency = wordFrequencies(spamSentences)
hamWordsFrequency = wordFrequencies(hamSentences)

for key, value in spamWordsFrequency.items():    
    if value == max(spamWordsFrequency.values()):
        print(key, value)   # print the most occurring word
        break

# Getting the probabilities
def calculateProbabilities(wordsAndFreq, totalWords, storeDictionary):
    for word, freq in wordsAndFreq.items():
        prob = freq / totalWords
        storeDictionary[word] = prob
    return storeDictionary
 

spamWordsProbs = {}
hamWordsProbs = {}

totalSpamWords = sum(spamWordsFrequency.values())
totalHamWords = sum(hamWordsFrequency.values())

calculateProbabilities(spamWordsFrequency, totalSpamWords, spamWordsProbs)
calculateProbabilities(hamWordsFrequency, totalHamWords, hamWordsProbs)

# Preparing methods for the testing strings

def iterate(string):
    spamProb = math.log(probSpam)
    hamProb = math.log(probHam)

    tokens = string.split()

    for item in tokens: # this part is equivalent to P(message|spam/ham) formula
        spamProb += math.log(spamWordsProbs.get(item, 1.0 / (totalSpamWords + 1)))
        hamProb += math.log(hamWordsProbs.get(item, 1.0 / (totalHamWords + 1)))
        # print(item, spamProb, hamProb)

    return spamProb, hamProb

def checkHamOrSpam(string): # if probability of spam is higher, then the message is a spam
    processed = process(string)
    spamProb, hamProb = iterate(processed)
    return 'spam' if spamProb > hamProb else 'ham'
# Test against the the testing part of our data set
testData['prediction'] = testData['processedTexts'].apply(checkHamOrSpam)
accuracy = accuracy_score(testData['spam'], testData['prediction'].map({'spam': 1, 'ham': 0}))
precision = precision_score(testData['spam'], testData['prediction'].map({'spam': 1, 'ham': 0}))

print(f'Accuracy: {accuracy}')
print(f'Precision: {precision}')
text = "Hey, I am free tomorrow. Drinks on me."
print(text, "\n This message is: ", checkHamOrSpam(text))
text = "Congratulations! You've won a $1,000 gift card. Click here to claim your prize now!"
print(text, "\n This message is: ", checkHamOrSpam(text))
