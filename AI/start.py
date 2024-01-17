import os
import random

import numpy as np

from keras.layers import Dense, SimpleRNN, Input, Embedding
from keras.models import Sequential
from keras.preprocessing.text import Tokenizer

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


with open('text.txt', 'r', encoding='utf-8') as f:
    texts = f.read()
    texts = texts.replace('\ufeff', '')

maxWordsCount = 250000
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

history = model.fit(X, Y, batch_size=64, epochs=35)


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
    try:
        incomes = int(input('Input your income: '))
        expenses = int(input('Input your expenses: '))
        categories = int(input('Input your spent on miscellaneous categories: '))
        recurring_expenses = int(input('Input your spent on recurring payments: '))
        savings = int(input('Input your spent on savings: '))
    except ValueError as e:
        if str(e).startswith("invalid literal for int() with base 10: 'stop'"):
            break
        else:
            print("Please enter a valid number.")
            continue

    advices_zero = [
        "It sounds like you're interested in improving your financial literacy. One valuable tip is to start tracking your expenses in more detail. This can be done using a budgeting app or a simple spreadsheet. By understanding where your money is going each month, you can identify areas where you may be overspending and adjust accordingly. Another key aspect is to educate yourself about personal finance. There are many free resources available online, including blogs, podcasts, and YouTube channels, which can offer valuable advice on saving, investing, and managing debt. Finally, setting clear financial goals can be a great motivator. Whether it's saving for a vacation, building an emergency fund, or investing for retirement, having specific targets can help you stay focused and make more informed financial decisions. Remember, improving financial literacy is a journey, and every small step you take can make a significant difference in the long run. Regards, Dowt.",
        "Hello, it's great to see your interest in my capabilities. Unfortunately, your statistics from the past month don't quite meet the necessary thresholds. However, I'm more than happy to offer you some advice on basic financial literacy for future reference: 1. Budgeting: The cornerstone of financial literacy is budgeting. Start by tracking your income and expenses. This will help you understand where your money is going and identify areas where you can cut back. There are many budgeting methods, like the 50/30/20 rule (50% on needs, 30% on wants, and 20% on savings), which can be a good starting point. 2. Emergency Fund: Building an emergency fund is crucial. Aim to save enough to cover 3-6 months of living expenses. This fund acts as a safety net for unexpected expenses, such as medical emergencies or job loss. 3. Understanding Debt: Learn about different types of debt - like credit card debt, student loans, and mortgages. Understanding interest rates and the terms of your debts is key to managing them effectively. Prioritize paying off high-interest debts first. 4. Investing Basics: While investing can seem daunting, understanding the basics is important for long-term financial health. Learn about different investment vehicles like stocks, bonds, and mutual funds. Remember, investing always involves risks, so it's crucial to do your research or consult with a financial advisor. 5. Retirement Planning: It's never too early to start thinking about retirement. Understand different retirement accounts like 401(k)s and IRAs, and take advantage of any employer match programs if available. 6. Credit Score: Your credit score is important for getting loans with favorable terms. Understand the factors that affect your credit score, like payment history and credit utilization, and work towards improving it. 7. Continuous Learning: The financial world is always evolving, so it's important to keep learning. Read books, follow financial news, and perhaps even take courses on personal finance. 8. Lifestyle Adjustments: Finally, be prepared to make adjustments to your lifestyle to live within your means. This might mean cutting back on non-essential expenses, looking for additional income sources, or reevaluating your financial goals. By incorporating these principles into your daily life, you'll be on your way to improved financial literacy and greater financial security. Remember, the key is consistency and willingness to learn and adapt. Your Dowt.",
        "Hi, I am very glad you are interested in my features, but unfortunately your stats for the last month are too low. However, for the future, I can give you advice on basic financial literacy: 1. Start with a Budget: Understanding where your money goes each month is crucial. Create a budget that outlines your income and expenses. This will help you see your spending habits and identify areas where you can save. 2. Build an Emergency Fund: Life is unpredictable. Aim to save enough to cover at least three to six months of expenses. This fund can be a lifesaver in case of unexpected events like job loss or medical emergencies. 3. Learn About Debt Management: Not all debt is bad, but understanding how to manage it is key. Prioritize paying off high-interest debts and be cautious about taking on new debts. Remember, paying debts on time can also improve your credit score. 4. Save and Invest Wisely: Even small amounts set aside regularly can grow over time. Look into savings accounts, retirement funds, and other investment options. It's important to start early and think long-term. 5. Educate Yourself Continuously: Financial literacy is an ongoing process. Read books, follow financial blogs, listen to podcasts, and attend workshops to stay informed about personal finance and investment strategies. 6. Set Realistic Financial Goals: Whether it's saving for a vacation, buying a house, or planning for retirement, setting clear financial goals can help you stay focused and motivated. By following these steps, you can improve your financial literacy and make more informed decisions about your money. Remember, taking control of your finances is a journey, and every step forward counts. Your financial advisor, Dowt."
    ]

    advices_incomes = [
        f"Hi. I'm glad you reached out to me for advice. According to last month, your income was ${incomes} dollars and your expenses were $0 dollars, I think: judging by your expenses you have enough resources to not spend money, that's great. You should keep an eye on your reserves to realize when you have less free money. By then you can have built up a sufficient safety cushion, this could be an amount that you have enough for 3-6 months of living without income. It may also be worth building up a portfolio of stable growth stocks to avoid inflation, this is important for gaining more financial independence. Regards, Dowt.",
        f"Hi. I'm glad you reached out to me for advice. According to last month, your income was ${incomes} dollars and your expenses were $0 dollars, I think: the fact that your income exceeds your expenses is great. You don't lose money shopping, but you should try to increase it. You can invest in non-risky stocks or start saving money to buy things that will help you earn more in the long run or to hire a tutor or mentor in the form of an authority figure to teach you new hard and soft skills to improve your skills and earnings. Regards, Dowt.",
        f"Hi. I'm glad you reached out to me for advice. According to last month, your income was ${incomes} dollars and your expenses were $0 dollars, I think: it is surprising that you refrain from spending while earning money. This could mean that you can provide enough comfort without spending, or perhaps you have a large stockpile of things you need. This is good for your financial wellbeing, but it might be worth investing your money or buying something that will help you earn more, rather than leaving it lying idle, then the money will not go to waste due to inflation, but will instead multiply. This approach would help you to have a big enough financial cushion in case of emergencies and problems in the future. Your financial advisor, Dowt."
    ]

    if incomes == 0 and expenses == 0:
        print(random.choice(advices_zero))
    elif incomes > 0 and expenses == 0:
        print(random.choice(advices_incomes))
    else:
        res = build_phrase(f"Hi. I'm glad you reached out to me for advice. According to last month, your income was ${incomes} dollars "
              f"and your expenses were ${expenses} dollars. Of that ${categories} dollars you spent on miscellaneous categories, "
              f"${recurring_expenses} dollars in recurring payments and ${savings} dollars in savings, I think:")
        print(res)
