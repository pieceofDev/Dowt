import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np

from keras.layers import Dense, SimpleRNN, Input, Embedding
from keras.models import Sequential
from keras.preprocessing.text import Tokenizer

with open('text.txt', 'r', encoding='utf-8') as f:
    texts = f.read()
    texts = texts.replace('\ufeff', '')

maxWordsCount = 1000
tokenizer = Tokenizer(num_words=maxWordsCount, filters='!–—#$%&()*+-/:;<=>?@[\\]^_`{|}~\t\n\r«»',
                      lower=True, split=' ', char_level=False)
tokenizer.fit_on_texts([texts])

dist = list(tokenizer.word_counts.items())
print(dist[:10])

data = tokenizer.texts_to_sequences([texts])
res = data[0]

inp_words = 3
n = len(res) - inp_words

X = np.array([res[i:i + inp_words] for i in range(n)])
Y = np.array(res[inp_words:])

model = Sequential()
model.add(Embedding(maxWordsCount, 256, input_length=inp_words))
model.add(SimpleRNN(128, activation='tanh', return_sequences=True))
model.add(SimpleRNN(64, activation='tanh'))
model.add(Dense(maxWordsCount, activation='softmax'))
model.summary()

model.compile(loss='sparse_categorical_crossentropy', metrics=['accuracy'], optimizer='adam')

history = model.fit(X, Y, batch_size=32, epochs=150)


def buildPhrase(texts, max_len=150):
    res = texts
    token_list = tokenizer.texts_to_sequences([texts])[0]
    while len(res.split()) < max_len:
        if len(token_list) < inp_words:
            break
        context = np.array(token_list[-inp_words:])
        context = np.expand_dims(context, axis=0)
        predicted_word_index = np.argmax(model.predict(context))
        predicted_word = tokenizer.index_word[predicted_word_index]
        if "dowt." in predicted_word:
            res += " " + predicted_word
            break
        res += " " + predicted_word
        token_list.append(predicted_word_index)
    sentences = res.split('. ')
    sentences_capitalized = [sentence.capitalize() for sentence in sentences]
    text_capitalized = '. '.join(sentences_capitalized)
    output = text_capitalized.replace("dowt.", "Dowt.")
    return output


res = buildPhrase("Hi. I'm glad you reached out to me for advice. According to last month, "
                  "your income was $400 dollars and your expenses were $200 dollars. Of that, "
                  "$100 dollars you spent on miscellaneous categories, $50 dollars on regular payments, "
                  "and $50 dollars on savings.")
print(res)
