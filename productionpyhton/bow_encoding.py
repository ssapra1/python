import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer  # Not used, but imported for other use cases
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer

# Read the CSV file and ensure columns are named 'label' and 'message'
try:
    data = pd.read_csv('spamclassification.csv', sep=',', names=['label', 'message'], on_bad_lines='skip')
except Exception as e:
    print("Error reading file: ", e)
    exit()

print(data)

# Download required NLTK data (uncomment the downloads if running for the first time)
# nltk.download('stopwords')
# nltk.download('wordnet')

corpus = []

# Instantiate WordNetLemmatizer (creating an object instance)
lemmatizer = WordNetLemmatizer()

for i in range(0, len(data)):
    # Clean the message by keeping only letters
    review = re.sub('[^a-zA-Z]', ' ', data['message'][i])
    review = review.lower()  # Convert to lowercase
    review = review.split()  # Tokenize into individual words

    # Lemmatize words, excluding any that are in the English stopwords
    review = [lemmatizer.lemmatize(word) for word in review if word not in stopwords.words('english')]

    # Join the cleaned words back into a single string
    cleaned_data = ' '.join(review)
    corpus.append(cleaned_data)


print(corpus)

cv = CountVectorizer(max_features=5,binary=True)


X=cv.fit_transform(corpus).toarray()
print(X)

print(X.shape)

##now we will talk about n grams

ngram_vectorizer = CountVectorizer(max_features=5,ngram_range=(3, 3))

X=ngram_vectorizer.fit_transform(corpus).toarray()
print(ngram_vectorizer.vocabulary_)
print(X)