import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')

from nltk.tokenize import sent_tokenize, word_tokenize


from nltk.stem import PorterStemmer

# Initialize the PorterStemmer
stemmer = PorterStemmer()

# Input sentence split into words
words = ["running", "runner", "ran", "easily", "studies", "studying"]

stems = [stemmer.stem(word) for word in words]
# Output the results
for word, stem in zip(words, stems):
    print(f"Original: {word} -> Stemmed: {stem}")

from nltk.stem import RegexpStemmer

stemmer=RegexpStemmer('ing$|s$|e$',min=4)

words = ["running", "runner", "ran", "easily", "studies", "studying"]

stems = [stemmer.stem(word) for word in words]
# Output the results
for word, stem in zip(words, stems):
    print(f"Original regex: {word} -> Stemmed regex: {stem}")



import  nltk.stem as WordNetLemmatizer
nltk.download('wordnet')
lamatizer=WordNetLemmatizer.WordNetLemmatizer()

words = ["running", "runner", "ran", "easily", "studies", "studying"]

for word in words:
    print('actual word is ' , word ,' and lamatized word is',lamatizer.lemmatize(word,''))

