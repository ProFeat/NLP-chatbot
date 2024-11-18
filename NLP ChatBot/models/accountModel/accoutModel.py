import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from nltk.corpus import stopwords
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import label_binarize
from nltk.stem import PorterStemmer

# Read CSV file
df = pd.read_csv("accountManager.csv")

# Separate question and intent columns
questions = df['Question']
intents = df['Intent']

# Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(questions, intents, test_size=0.2, random_state=42)

# Define text processing and classification pipeline with SVM
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

text_clf = Pipeline([
    ('vect', CountVectorizer(stop_words=list(stop_words))),
    ('tfidf', TfidfTransformer()),
    ('clf', SVC())  # Use default SVM for now
])

# Define hyperparameter grid
param_grid = {
    'clf__C': [0.1, 1, 10, 100],  # Regularization parameter
    'clf__kernel': ['linear', 'rbf', 'poly'],  # Kernel type
}

# Use GridSearchCV to search for best hyperparameters
grid_search = GridSearchCV(text_clf, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

# Get the best hyperparameters
best_params = grid_search.best_params_
print(f"Best Hyperparameters: {best_params}")

# Evaluate the model with the best hyperparameters on the test set
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy with Best Hyperparameters: {accuracy}")

# Classification Report
classification_rep = classification_report(y_test, y_pred)
print("Classification Report:")
print(classification_rep)

# Confusion Matrix
conf_mat = confusion_matrix(y_test, y_pred)

# Plot Confusion Matrix with adjusted size and font size
plt.figure(figsize=(10, 8))
sns.heatmap(conf_mat, annot=True, fmt='d', cmap='Blues', xticklabels=best_model.classes_, yticklabels=best_model.classes_, annot_kws={"size": 10})
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix')
plt.show()

# Save the trained model to a file
model_filename = 'account_model_svm.pkl'
joblib.dump(best_model, model_filename)
print(f"Trained model saved to {model_filename}")

# Example usage:
user_input = input("Enter your question: ")

# Load the trained model from the file
loaded_model = joblib.load(model_filename)

# Use the loaded model for prediction
predicted_intent = loaded_model.predict([user_input])
print(f"Predicted Intent: {predicted_intent[0]}")
