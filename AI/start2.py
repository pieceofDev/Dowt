import os

import numpy as np

from keras.layers import Dense, Embedding
from keras.models import Sequential
from keras.preprocessing.text import Tokenizer
from keras.src.layers import LSTM, Bidirectional

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


# Открытие файла с использованием конструкции with для автоматического закрытия файла после завершения операций
with open('text.txt', 'r', encoding='utf-8') as f:
    texts = f.read()
    texts = texts.replace('\ufeff', '')  # Удаление ненужных символов

maxWordsCount = 21000

# Обновленная конфигурация токенизатора
tokenizer = Tokenizer(num_words=maxWordsCount, filters='',
                      lower=True, split=' ', char_level=False)
tokenizer.fit_on_texts([texts])

# Вывод небольшого отрывка из списка слов
dist = list(tokenizer.word_counts.items())
print(dist[:10])

# Преобразование текста в последовательность чисел
data = tokenizer.texts_to_sequences([texts])
res = data[0]

inp_words = 40
n = len(res) - inp_words

X = np.array([res[i:i + inp_words] for i in range(n)])
Y = np.array(res[inp_words:])

model = Sequential()
model.add(Embedding(maxWordsCount, 256, input_length=inp_words))
model.add(LSTM(128, activation='tanh', return_sequences=True))
model.add(Bidirectional(LSTM(64, activation='tanh')))  # Добавление слоя Bidirectional LSTM
model.add(Dense(maxWordsCount, activation='softmax'))
model.summary()

model.compile(loss='sparse_categorical_crossentropy', metrics=['accuracy'], optimizer='adam')

history = model.fit(X, Y, batch_size=32, epochs=150)


def build_phrase(texts, max_len=500):
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


# res = build_phrase("Hi. I'm glad you reached out to me for advice. According to last month, your income was $2355 dollars "
#                    "and your expenses were $1234 dollars. Of the $223 dollars you spent on miscellaneous categories, "
#                    "$777 dollars in recurring payments and $234 dollars in savings, I think")
# print(res)

while True:
    phrase_begin = input("You can put data: ")
    result = build_phrase(phrase_begin)
    print(result)
    if phrase_begin.lower() == "stop":
        break
