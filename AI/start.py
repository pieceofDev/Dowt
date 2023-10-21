import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np

from keras.layers import Dense, SimpleRNN, Input
from keras.models import Sequential
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical

with open('text', 'r', encoding='utf-8') as f:
    texts = f.read()
    texts = texts.replace('\ufeff', '')

maxWordsCount = 1000

tokenizer = Tokenizer(num_words=maxWordsCount, filters='!-"@#$%^&*()', lower=True, split='', char_level=False)

tokenizer.fit_on_texts([texts])

dist = list(tokenizer.word_counts.items())
