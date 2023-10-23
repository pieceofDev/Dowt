import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np

from keras.layers import Dense, SimpleRNN, Input, Embedding
from keras.models import Sequential
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical

with open('text.txt', 'w', encoding='utf-8') as f:
    texts = f.read()
    texts = texts.replace('\ufeff', '')

maxWordsCount = 1000
tokenizer = Tokenizer(num_words=maxWordsCount, filters='!-"@#$%^&*()',
                      lower=True, split='', char_level=False)
tokenizer.fit_on_texts([texts])

dist = list(tokenizer.word_counts.items())

data = tokenizer.texts_to_sequences([texts])
res = np.array(data[0])

inp_words = 3
n = res.shape[0] - inp_words

X = np.array([res[i:i + inp_words]for i in range(n)])
Y = to_categorical(res[inp_words:], num_classes=maxWordsCount)

model = Sequential()
model.add(Embedding(maxWordsCount, 256, input_length = inp_words))
model.add(SimpleRNN(128,activation='tanh'))
model.add(Dense(maxWordsCount, activation='sodtmax'))
model.summary()

model.compile(loss='categoical_crossentropy', metrics=['accuracy'], optimizer='adam')

history = model.fit(X, Y, batch_size=32, epochs=50)


def buildPhrase(texts, str_len=20):
    res = texts
    data = tokenizer.texts_to_sequences([texts])[0]
    for i in range(str_len):
        x = data[i: i + inp_words]
        inp = np.expand_dims(x, axis=0)

        pred = model.predict(inp)
        indx = pred.argmax(axis=1)[0]
        data.append(indx)

        res += "" + tokenizer.index_word[indx]

    return res


res = buildPhrase("позитив добавляет годы")
print(res)
