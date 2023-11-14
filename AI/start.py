import os

import numpy as np

from keras.layers import Dense, SimpleRNN, Input, Embedding
from keras.models import Sequential
from keras.preprocessing.text import Tokenizer

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


with open('text.txt', 'r', encoding='utf-8') as f:
    texts = f.read()
    texts = texts.replace('\ufeff', '')

maxWordsCount = 21000
tokenizer = Tokenizer(num_words=maxWordsCount, filters='',
                      lower=True, split=' ', char_level=False)
tokenizer.fit_on_texts([texts])

dist = list(tokenizer.word_counts.items())
print(dist[:10])

data = tokenizer.texts_to_sequences([texts])
res = data[0]

inp_words = 40
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

history = model.fit(X, Y, batch_size=32, epochs=100)


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


while True:
    incomes = int(input('Input your income: '))
    expenses = int(input('Input your expenses: '))
    categories = int(input('Input your spent on miscellaneous categories: '))
    recurring_expenses = int(input('Input your spent on recurring payments: '))
    savings = int(input('Input your spent on savings: '))
    # Изменил список на множество (скобки), потому-что множество более оптимизировано, а также мы можем просто брать первый элемент из него, он всегда будет разным, это особенность питона, потому-что во множестве не важно в каком порядке стоят элементы
    advices_zero = {
        ""
        ""
        ""
    }

    advices_incomes = {
        ""
        ""
        ""
    }

    if any([i.lower == "stop" for i in [incomes, expenses, categories, recurring_expenses, savings]]):
        break

    if incomes == 0 and expenses == 0:
        print(advices_zero[0])
    elif incomes > 0 and expenses == 0:
        print(advices_incomes[0])
    else:
        res = build_phrase(f"Hi. I'm glad you reached out to me for advice. According to last month, your income was ${incomes} dollars "
              f"and your expenses were ${expenses} dollars. Of the ${categories} dollars you spent on miscellaneous categories, "
              f"${recurring_expenses} dollars in recurring payments and ${savings} dollars in savings, I think:")
        print(res)
