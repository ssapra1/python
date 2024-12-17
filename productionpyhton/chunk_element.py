

import nltk

from nltk import sent_tokenize,word_tokenize
nltk.download('maxent_ne_chunker_tab')
nltk.download('words')
nltk.download('averaged_perceptron_tagger_eng')
sentence = "The quick brown fox jumps over the lazy dog, TAJ MAHAL"

tokenize_words=word_tokenize(sentence)
print(tokenize_words)
tag_words=nltk.pos_tag(tokenize_words)

print(tag_words)
chunk_words=nltk.ne_chunk(tag_words).draw()

print(chunk_words)