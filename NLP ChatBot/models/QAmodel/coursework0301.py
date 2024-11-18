import csv
import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib

qa_FILEPATH = 'QAS.csv' 
qaData = []

with open(qa_FILEPATH, 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)  # 读取CSV文件的头部
    for row in csv_reader:
        if len(row) == 4:  # 确保每行都有四列
            question_id, question, answer, document = row
            qaData.append((question_id, question, answer, document))
        else:
            print(f"Warning: Skipped row with incorrect format: {row}")

vectorizer = CountVectorizer()

# 拟合（fit）向量化器
vectorizer.fit([f"{question} {answer}" for _, question, answer, _ in qaData])

# 保存 CountVectorizer 的状态
joblib.dump(vectorizer, 'QAcount_vectorizer.joblib')

# 使用NLTK进行预处理
userInput = ' '.join(word_tokenize("What are stocks and BONDS".lower()))

# 使用向量化的方法进行意图匹配
vectorized_intents = vectorizer.transform([userInput] + [f"{question} {answer}" for _, question, answer, _ in qaData])
similarities = cosine_similarity(vectorized_intents)[0]
max_similarity_index = similarities[1:].argmax()

# 如果最大相似度超过阈值，返回相似意图的索引，否则返回None
if similarities[max_similarity_index + 1] > 0.5:
    print(f"Chatbot: {qaData[max_similarity_index][2]}")

# 从文件中加载 CountVectorizer 的状态
loaded_vectorizer = joblib.load('QAcount_vectorizer.joblib')
# 可以使用 loaded_vectorizer.transform() 来对新的文本进行向量化
