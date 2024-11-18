from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
from nltk.tokenize import word_tokenize
import csv

# 读取数据集
dataset_file = 'smallTalk.csv'
smallTalkData = []

with open(dataset_file, 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)  # 读取CSV文件的头部
    for row in csv_reader:
        if len(row) == 2:  # 确保每行都有两列
            question, intent = row
            smallTalkData.append((question, intent))
        else:
            print(f"Warning: Skipped row with incorrect format: {row}")

# 使用 CountVectorizer 进行向量化
vectorizer = CountVectorizer()
vectorizer.fit([f"{question}" for question, _ in smallTalkData])

# 保存 CountVectorizer 的状态
joblib.dump(vectorizer, 'smallTalk_vectorizer.joblib')

# 使用NLTK进行预处理
user_input = ' '.join(word_tokenize("What can you do".lower()))

# 使用向量化的方法进行意图匹配
vectorized_intents = vectorizer.transform([user_input] + [f"{question}" for question, _ in smallTalkData])
similarities = cosine_similarity(vectorized_intents)[0]
max_similarity_index = similarities[1:].argmax()

# 如果最大相似度超过阈值，返回相似意图的索引，否则返回None
if similarities[max_similarity_index + 1] > 0.5:
    print(f"Small Talk Intent: {smallTalkData[max_similarity_index][1]}")

# 保存小聊数据
smallTalkData_dict = {'vectorizer': vectorizer, 'intents': smallTalkData}
joblib.dump(smallTalkData_dict, 'smallTalk_data.joblib')

