from User import User
from UserDBManager import UserDatabase
from UserAccountManager import AuthenticationManager
from RestrautantBook import run_main

import os
import csv
import joblib
from datetime import datetime
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

'''
user login or register
'''
def registerUser(authManager, user):

    success, message = authManager.registerUser(user)
    return success, message

def loginUser(authManager,user):
    success, message, userData = authManager.loginUser(user)
    return success, message, userData

def handleRegistrationFailure(message):
    # Perform different operations based on different failure messages
    if "Invalid email format" in message:
        print("Invalid email format. Please enter a valid email.")
        
    elif "Email already exists" in message:
        print("Email already exists. Please use a different email.")
        
    else:
        
        print(f"Registration failed: {message}")

def handleLoginFailure(message, authManager, user):
    if "Invalid email format" in message:
        print("Invalid email format")
    elif "Email does not exist" in message:
        print("Email does not exist")
        choice = input("Do you want to register (yes/no): ")
        if choice.lower() == "yes":
            userName = input("Enter username: ")
            user.setUserName(userName)
            success, message = registerUser(authManager, user)
            print(message)
            if success:
                print("User registered successfully")
            else:
                # Handle registration failure
                handleRegistrationFailure(message)
                return False  #  False, not break
        elif choice.lower() == "no":
            # no ,true ,break
            print("Exiting the program.")
            return True
        else:
            print("Invalid choice. Please enter 'yes'or 'no'.")

    elif "Incorrect password" in message:
        print("Incorrect password")
    else:
        print(f"Login failed: {message}")
    
    return False  # false , not break

'''
greeting
'''
def getGreeting(lastLoginTime):
    currentTime = datetime.now().time()

    if currentTime < datetime.strptime("12:00", "%H:%M").time():
        greetingStr = "Good morning!"
    elif currentTime < datetime.strptime("18:00", "%H:%M").time():
        greetingStr =  "Good afternoon!"
    else:
        greetingStr = "Good evening!"
    
    if lastLoginTime is None:
        # If you are logging in for the first time, a welcome message is displayed
        return greetingStr + "Welcome!"
    
    # Convert lastLoginTime to a datetime.time object
    lastLoginTime = datetime.strptime(lastLoginTime, "%H:%M:%S").time()

    # Calculate the time difference since last login
    timeDifference = datetime.combine(datetime.today(), currentTime) - datetime.combine(datetime.today(), lastLoginTime)

    # Set different greetings according to the time difference
    if timeDifference.days == 0 and timeDifference.seconds < 60 * 60:  #less 1h
        return greetingStr + "Welcome back! Nice to see you again. It's been less than an hour."
    elif timeDifference.days == 0:
        return f"{greetingStr}Welcome back! How may I help you today? It's been {timeDifference.seconds // 3600} hours since your last visit."
    else:
        return f"{greetingStr}Welcome back! Long time no see, and I've missed you. It's been {timeDifference.days} days since your last visit."

'''
QA and processtext
'''
def preprocessText(text):
    #Use NLTK for text preprocessing, including word segmentation and lowercase.
    tokens = word_tokenize(text.lower())
    return ' '.join(tokens) 

def loadData(FILEPATH):
    #Load QA data from the CSV file and return a list of questions, answers, and more.
    qaData = []
    with open(FILEPATH, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  
        for row in csv_reader:
            if len(row) == 4:  # Make sure that each row has four columns
                question_id, question, answer, document = row
                qaData.append((question_id, question, answer, document))
            else:
                print(f"Warning: Skipped row with incorrect format: {row}")
    return qaData

# Define intent-to-output mapping dictionary
intent_mapping = {
    "smalltalk_agent_acquaintance": "Nice to meet you! I can help you with simple restaurant reservations, account management and answer limited questions",
    "smalltalk_agent_talk_to_me": "Of course! What would you like to talk about?",
    "smalltalk_appraisal_good": "That's great to hear!",
    "smalltalk_appraisal_bad": "I'm sorry to hear that. How can I help?",
    "smalltalk_appraisal_thank_you": "You're welcome!",
    "smalltalk_appraisal_welcome": "You're welcome! How can I assist you?",
    "smalltalk_greetings_bye": "Goodbye! If you need anything, I'll be here.",
    "smalltalk_greetings_goodevening": "Good evening! How can I assist you?",
    "smalltalk_greetings_goodmorning": "Good morning! What can I do for you today?",
    "smalltalk_greetings_goodnight": "Good night! Have a restful sleep.",
    "smalltalk_greetings_hello": "Hello! How can I assist you today?",
    "smalltalk_greetings_how_are_you": "I'm doing well, thank you! How about you?",
    "smalltalk_greetings_nice_to_meet_you": "Nice to meet you too!",
    "smalltalk_greetings_nice_to_see_you": "Nice to see you! How can I help?",
    "smalltalk_greetings_nice_to_talk_to_you": "It's nice talking to you! What can I do for you?",
    "smalltalk_user_going_to_bed": "Good night! Sleep well!",
    "smalltalk_user_sleepy": "If you're feeling sleepy, maybe it's time for a break.",

}


def main():
    # Get the path of the current script
    currentDirectory = os.path.dirname(os.path.abspath(__file__))
    
    # Create a user database and specify a relative path
    db_path = os.path.join(currentDirectory, 'Database.db')
    userDB = UserDatabase(dbPath=db_path)
    # The default logout time is None or other default value
    newUser = User(None, None, None, None, None)
    # Create user authentication manager
    authManager = AuthenticationManager(userDB)
    
    mainModelSubdirectory = 'models/mainModel'
    QAModelSubdirectory = 'models/QAModel'
    accoutModelSubdirectory = 'models/accountModel'
    smallTalkModelSubdirectory =  "models/smallTalkModel"
    # Construct the full paths for the model and vectorizer
    model_filename = os.path.join(mainModelSubdirectory, 'main_classifier_model.joblib')
    vectorizer_filename = os.path.join(mainModelSubdirectory, 'main_vectorizer.joblib')
    QAcount_vectorizer_filename = os.path.join(QAModelSubdirectory,'QAcount_vectorizer.joblib')
    QAData_path = os.path.join(QAModelSubdirectory, 'COMP3074-CW1-Dataset.csv')
    accoutMoodel_filename = os.path.join(accoutModelSubdirectory, 'accout_model_svm.pkl')
    smallTalk_vectorizer_filename = os.path.join(smallTalkModelSubdirectory,'smallTalk_vectorizer.joblib')
    samllTall_data_filename = os.path.join(smallTalkModelSubdirectory, 'smallTalk_data.joblib')

    # Load the model and vectorizer
    loaded_classifier = joblib.load(model_filename)
    loaded_vectorizer = joblib.load(vectorizer_filename)
    print(f"Loaded Vectorizer Feature Count: {loaded_vectorizer.get_feature_names_out().shape[0]}")

    loaded_QAvectorizer = joblib.load(QAcount_vectorizer_filename)

    loaded_smallTalkV = joblib.load(smallTalk_vectorizer_filename)
    loaded_smallTalkData = joblib.load(samllTall_data_filename)


    loaded_accoutclassifier = joblib.load(accoutMoodel_filename)

    qaData = loadData(QAData_path)

    EXIT_PROGRAM = False  # exit 

    try:
        while True:  
            choice = input("Do you have an account? (yes/no/exit): ")

            if choice.lower() == "yes":
                print("Login:")
                email = input("Enter email: ")
                password = input("Enter password: ")

                newUser.setUserEmail(email)
                newUser.setPassword(password)

                success, message, userData = loginUser(authManager,newUser)
                if success:
                    print("User information:")
                    print(userData.get("userName"))
                    # print(userData)
                    newUser.setFromDict(userData)
                    greeting = getGreeting(newUser.getLogoutTime())

                    # prit greeting
                    print(greeting)
                    break  # Exit loop after successful login
                else:
                    # Handle login failure
                    EXIT_PROGRAM = handleLoginFailure(message, authManager, newUser)
                    if EXIT_PROGRAM == True:
                        break
            elif choice.lower() == "no":
                print("Register a new user:")
                userName = input("Enter username: ")
                email = input("Enter email: ")
                password = input("Enter password: ")

                newUser.setUserName(userName)
                newUser.setPassword(password)
                newUser.setUserEmail(email)

                success, message = registerUser(authManager, newUser)
                print(message)
                if success:
                    print("User registered successfully")
                else:
                    # Handle registration failure
                    handleRegistrationFailure(message)
            elif choice.lower() == "exit":
                print("Exiting the program.")
                # true break
                EXIT_PROGRAM = True
                break
            else:
                print("Invalid choice. Please enter 'yes', 'no', or 'exit'.")

        
        if EXIT_PROGRAM:
            print("Additional operations after exiting the system.")
            return
        
        print(newUser)
        
        # while not EXIT_PROGRAM:
        while True:
            userConversation = input("hello: ")
            preuserCoversation = preprocessText(userConversation)
            
            '''
            Small Talk
            '''
            vectorized_user_input = loaded_smallTalkV.transform([preuserCoversation]+ [f"{question}" for question, _ in loaded_smallTalkData['intents']])
            similarities = cosine_similarity(vectorized_user_input)[0]
            max_similarity_index = similarities[1:].argmax()

            # Return the index of similar intent if the maximum similarity exceeds the threshold, otherwise None
            if similarities[max_similarity_index + 1] > 0.9:
                matched_intent = loaded_smallTalkData['intents'][max_similarity_index][1]
                # Use a dictionary map to get the corresponding output
                output_message = intent_mapping.get(matched_intent, f"Small Talk Intent: {matched_intent}")
                print(output_message)
                continue
            '''
            QASearch
            '''

            # Vectorized user input
            vectorizedPreuserCoversation = loaded_QAvectorizer.transform([preuserCoversation])
            # Vectorize all questions
            all_questions = [question for _, question, _, _ in qaData]
            vectorized_intents = loaded_QAvectorizer.transform([preprocessText(question) for question in all_questions])
            # Calculate similarity
            similarities = cosine_similarity(vectorizedPreuserCoversation, vectorized_intents)
            # Get an index of the most similar questions
            max_similarity_index = similarities[0,1:].argmax()
            # If the maximum similarity exceeds the threshold, return the index of similar intent, otherwise None
            threshold = 0.5 
            if similarities[0, max_similarity_index + 1] > threshold:
                print(f"Chatbot: {qaData[max_similarity_index +1][2]}")
                continue

            '''
            System EXIT
            '''
            keywords = ["Systembreak", "Systemend","break",  "exit", "quit", "end"]
            if any(keyword in userConversation for keyword in keywords):
                currentTimeStr = datetime.now().time().strftime("%H:%M:%S")
                newUser.setLogoutTime(currentTimeStr)
                authManager.updateUserInfo(newUser)
                print(newUser)
                break
                # EXIT_PROGRAM = True

            '''
            Account and Resturant
            '''
            # Use the loaded vectorizer to process user input
            user_input_features = loaded_vectorizer.transform([userConversation])
            # print(f"User Input Features Shape: {user_input_features.shape}")

            # Use the loaded classifier for prediction
            prediction = loaded_classifier.predict(user_input_features)
            if prediction == 0:
                print("Welcome to restaruant book manager")
                run_main()
            elif prediction == 1:
                print("Welcome to account manager")
                predicted_intent = loaded_accoutclassifier.predict([userConversation])
                cleaned_intent = predicted_intent[0].strip(' "')
                cleaned_intent = cleaned_intent.strip("'")  # remove " ' ""
                # print(f"Cleaned Intent: {cleaned_intent!r}")

                if(cleaned_intent == "user_account_change_password"):
                    inputPassword = input("Please Input Pasword")
                    newUser.setPassword(inputPassword)
                    success, message = authManager.updateUserInfo(newUser)
                    if success:
                        print(message)
                    else:
                        print(message)
                elif(cleaned_intent == "user_account_change_username"):
                    inputUserName = input("Please Input Udername ")
                    newUser.setUserName(inputUserName)
                    success, message = authManager.updateUserInfo(newUser)
                    if success:
                        print(message)
                    else:
                        print(message)
                elif(cleaned_intent == "user_account_change_email"):
                    inputEmail = input("Please Input Email ")
                    newUser.setUserEmail(inputEmail)
                    success, message = authManager.updateUserInfo(newUser)
                    if success:
                        print(message)
                    else:
                        print(message)
                elif(cleaned_intent == "user_info_query"):
                    success, message, userData = authManager.queryUserInfo(newUser.getEmail())
                    if success:
                        # print(userData)
                        for key in userData:
                            print(f"{key} : {userData[key]}")
                    else:
                        print(message)
                else:
                    "Sorry"
    finally:
        # Close the database connection at the end of the program
        userDB.closeConnection()

if __name__ == "__main__":
    main()
