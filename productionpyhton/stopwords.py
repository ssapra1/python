import nltk
from nltk import sent_tokenize

from nltk.stem import WordNetLemmatizer

from nltk.corpus import stopwords


nltk.download('stopwords')
stop_words = stopwords.words('english')
nltk.download('punkt')
stop_words=stop_words.append('country, army')
print(stop_words)



from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize,sent_tokenize
nltk.download('punkt_tab')
sentence= 'The great missile man becomes the President of India in 2002. During his presidency period, the army and country achieved many milestones that contributed a lot to the nation. He served the nation with an open heart that’s why he was called ‘people’s president’. But at the end of his term period, he was not satisfied with his work that’s why he wanted to be the President a second time but later on forfeited his name.'

stemmer=PorterStemmer()
lamatizer=WordNetLemmatizer()

tokens = sent_tokenize(sentence)
print(tokens)

for i in range(len(tokens)):
    words = word_tokenize(tokens[i])
    words1=[lamatizer.lemmatize(word.lower()) for word in words if word not in set(stop_words)]
    tokens[i]=' '.join(words1)

print(tokens)

