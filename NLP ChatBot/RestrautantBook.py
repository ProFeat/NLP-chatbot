import nltk
from nltk.tokenize import word_tokenize
from datetime import datetime, timedelta
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


from Restaurant import Restaurant
from RestaurantDBManager import RestaurantDatabaseManager
from RestaurantManager import RestaurantManager

nltk.download('punkt')
nltk.download('stopwords')


should_exit = 0

'''
precess
'''
def preprocess_user_input(user_input):
    # 分词
    words = word_tokenize(user_input.lower())

    # 移除停用词
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]

    return filtered_words

'''
time
'''
def is_valid_year(value):
    try:
        year = int(value)
        return 1900 <= year <= 2100
    except ValueError:
        return False

def is_valid_month(month):
    return month.lower() in ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

def is_valid_day(value):
    try:
        day = int(value)
        return 1 <= day <= 31  
    except ValueError:
        return False

def parse_relative_date(relative_date):
    today = datetime.today()
    weekdays = {
        'monday': 0, 'tuesday': 1, 'wednesday': 2,
        'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6
    }

    words = nltk.word_tokenize(relative_date.lower())
    for w in words:
        if w in weekdays:
            weekday = weekdays[w]
            days_until = (weekday - today.weekday() + 7) % 7
            result_date = today + timedelta(days=days_until)
            return result_date

#     return None

def complete_date(words):
    # words = nltk.word_tokenize(text)
    key_dates = {'today': 0, 'tomorrow': 1, 'day after tomorrow': 2}
    date_parts = {'year': None, 'month': None, 'day': None}

    for i, w in enumerate(words):
        if w.lower() in key_dates:
            date_parts['year'] = (datetime.today() + timedelta(days=key_dates.get(w.lower(), 0))).year
            date_parts['month'] = (datetime.today() + timedelta(days=key_dates.get(w.lower(), 0))).month
            date_parts['day'] = (datetime.today() + timedelta(days=key_dates.get(w.lower(), 0))).day
        elif w.lower() in ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']:
            date_parts['month'] = w  # 保留月份的原始字符串
        elif w.isdigit():
            # 判断是年份还是日期
            value = int(w)
            if date_parts['year'] is None and is_valid_year(value):
                date_parts['year'] = value
            elif date_parts['day'] is None and is_valid_day(value):
                date_parts['day'] = value
        elif w.lower() in ['this', 'next'] and i + 1 < len(words) and words[i + 1] in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            result_date = parse_relative_date(words[i + 1])
            if result_date:
                return {'year': result_date.year, 'month': result_date.strftime('%B'), 'day': result_date.day}


    missing_parts = []
    # Check if the date section is missing
    for part, value in date_parts.items():
        if value is None or (part == 'year' and not is_valid_year(value)) or (part == 'month' and not is_valid_month(value)) or (part == 'day' and not is_valid_day(value)):
            missing_parts.append(part)

    # Prompt the user for the missing date section and re-enter
    for part in missing_parts:
        user_input = input(f"Please provide the {part} you want to book: ")
        if part == 'year' and is_valid_year(user_input):
            date_parts['year'] = user_input
        elif part == 'month' and is_valid_month(user_input):
            date_parts['month'] = user_input
        elif part == 'day' and is_valid_day(user_input):
            date_parts['day'] = user_input
        else:
            # If user input is not valid, continue the loop until valid data is entered
            while True:
                user_input = input(f"Invalid input for {part}. Please provide a valid {part}: ")
                if (part == 'year' and is_valid_year(user_input)) or (part == 'month' and is_valid_month(user_input)) or (part == 'day' and is_valid_day(user_input)):
                    date_parts[part] = user_input
                    break

    return date_parts

'''
intent
'''


def luxury_intent(restaurant):
    
    print("Executing luxury_intent operation.")
    restaurant.setRoomName("VIP room")
    return "Luxury Intent Operation"

def standard_intent(restaurant):
    print("Executing standard_intent operation.")
    restaurant.setRoomName("Standard room")
    return "Standard Intent Operation"

def large_room_intent(restaurant):
    print("Executing large_room_intent operation.")
    restaurant.setSizes('Max')
    return "Large Room Intent Operation"

def medium_room_intent(restaurant):
    print("Executing medium_room_intent operation.")
    restaurant.setSizes('Medium')
    return "Medium Room Intent Operation"

def small_room_intent(restaurant):
    print("Executing small_room_intent operation.")
    restaurant.setSizes('Small')
    return "Small Room Intent Operation"

def restaurant_a_intent(restaurant):
    print("Executing Restaurant A intent operation.")
    restaurant.setRestaurantName('RestaurantA')
    return "Restaurant A Intent Operation"

def restaurant_b_intent(restaurant):
    print("Executing Restaurant B intent operation.")
    restaurant.setRestaurantName('RestaurantB')
    return "Restaurant B Intent Operation"

def restaurant_c_intent(restaurant):
    print("Executing Restaurant C intent operation.")
    restaurant.setRestaurantName('RestaurantC') 
    return "Restaurant C Intent Operation"

def high_price_intent(restaurant):
    print("Executing high_price_intent operation.")
    restaurant.setExpectedPrice('high price')
    return "High Price Intent Operation"

def medium_price_intent(restaurant):
    print("Executing medium_price_intent operation.")
    restaurant.setExpectedPrice('moderate price')  
    return "Medium Price Intent Operation"

def low_price_intent(restaurant):
    print("Executing low_price_intent operation.")
    restaurant.setExpectedPrice('low price')
    return "Low Price Intent Operation"

def cancel_intent(restaurant):
    global should_exit
    print("Executing cancel_intent operation.")
    should_exit = 1
    return "Cancel Intent Operation"

def modify_intent(restaurant):
    global should_exit
    print("Executing modify_intent operation.")
    restaurant.setToNone()
    should_exit = 2
    return "Modify Intent Operation"

def confirm_intent(restaurant):
    global should_exit
    print("Executing confirm_intent operation.")
    should_exit = 3
    return "confirm Intent Operation"

def unknown_intent(restaurant):
    print("Executing unknown_intent operation.")
    
    return "Unknown Intent Operation"


intent_keyword_mapping =  {
    'luxury': ['luxury', 'deluxe', 'premium', 'vip', 'exclusive', 'elegant', 'lavish'],
    'standard': ['standard', 'regular', 'basic', 'normal', 'ordinary'],
    'largeRoom': ['large',  'spacious', 'deluxe', 'suite', 'big', 'roomy', 'generous'],
    'mediumRoom': ['medium',  'standard', 'mid-sized', 'suite', 'moderate-sized', 'average'],
    'smallRoom': ['small',  'compact', 'petite', 'suite', 'cozy', 'intimate'],
    'restaurantA': ['restauranta'],
    'restaurantB': ['restaurantb'],
    'restaurantC': ['restaurantc'],
    'highPrice': ['high',  'expensive', 'premium', 'luxury', 'upscale', 'costly', 'pricy'],
    'mediumPrice': ['moderate',  'standard', 'cost' , 'average', 'rate', 'regular', 'pricing', 'affordable'],
    'lowPrice': ['low', 'affordable', 'budget-friendly', 'economical', 'cheap', 'inexpensive'],
    'cancel': ['cancel', 'withdraw', 'revoke', 'terminate', 'call', 'off', 'abort'],
    'modify': ['modify', 'change', 'alter', 'adjust', 'amend', 'edit'],
    'confirm': ['confirm', 'reservation', 'approve', 'verify', 'accept', 'acknowledge']
    # 'confirm': ['confirm', 'withdraw', 'reservation', 'revoke', 'booking'],
}



intent_functions = {
    'luxury': luxury_intent,
    'standard': standard_intent,
    'largeRoom': large_room_intent,
    'mediumRoom': medium_room_intent,
    'smallRoom': small_room_intent,
    'restaurantA': restaurant_a_intent,
    'restaurantB': restaurant_b_intent,
    'restaurantC': restaurant_c_intent,
    'highPrice': high_price_intent,
    'mediumPrice': medium_price_intent,
    'lowPrice': low_price_intent,
    'cancel': cancel_intent,
    'modify': modify_intent,
    'confirm': confirm_intent,
}

def generate_intent_statements(words, intent_keyword_mapping, intent_functions, restaurant):
    matched_intents = []  # Used to store the intent of the match
    print(words)
    for intent, keywords in intent_keyword_mapping.items():
        # If any keyword is matched successfully, the entire intent is considered to be matched successfully
        if any(keyword in word for keyword in keywords for word in words):
            result = intent_functions.get(intent, unknown_intent)(restaurant)
            matched_intents.append({
                'intent': intent,
                'result': result
            })

    return matched_intents


def run_main():
    # Create a database manager instance
    dbManager = RestaurantDatabaseManager()

    # Create a restaurant manager instance and insert 10 restaurants
    restaurantManager = RestaurantManager(dbManager, numRestaurants=10)
    temRestaurant = Restaurant()
    temRestaurant.setIsReserved(0)
    bookTime = None
    global should_exit
    # while should_exit == 0 or should_exit == 2 or temRestaurant.isComplete():
    while should_exit == 0 or should_exit == 2:
        userInput = input("Please Input：")
        preUserInput = preprocess_user_input(userInput)
        matched_intents = generate_intent_statements(preUserInput, intent_keyword_mapping, intent_functions, temRestaurant)
        print(temRestaurant.toDict())

        if should_exit == 1:
            break  
        elif should_exit == 2:
            # global should_exit
            should_exit = 0
            bookTime = None
            # temRestaurant.setIsReserved(1)
            continue
        elif should_exit == 3:
            temRestaurant.setReservedTime(bookTimeToStr)
            temRestaurant.setIsReserved(1)
            dbManager.insertRestaurant(temRestaurant)
            break

        if bookTime is None:
            bookTime = complete_date(preUserInput)
            bookTimeToStr = f"Date: {bookTime['year']}/{bookTime['month']}/{bookTime['day']}"
            print(bookTimeToStr)

        found_restaurant = restaurantManager.findRestaurantByAttribute(temRestaurant)  # 调用函数查询餐厅
        if found_restaurant is None:
            print("Sorry,There are no eligible rooms")
            continue

        filtered_restaurants = []
        for restaurant in found_restaurant:
            if not (restaurant.get("isReserved") == 1 and restaurant.get("reservedTime") == bookTime):
                filtered_restaurants.append(restaurant)

        
        found_restaurant = filtered_restaurants

        temNonEmptyAttributes = temRestaurant.toDict()
        NonEmptyAttributes = {
            key: value
            for key, value in temNonEmptyAttributes.items()
            if key != "isReserved" and value is not None and value != ''
        }
        EmptyAttributes = {
            key: value
            for key, value in temNonEmptyAttributes.items()
            if key != 'roomID' and (value is None or value == '') and key != "reservedTime"
        }
        # description = ", ".join(f"符合{key}是{value}" for key, value in NonEmptyAttributes.items())
        # nonDescription =  ", ".join(f"还缺少{key}条件" for key,value in EmptyAttributes.items())

        description = ""
        nonDescription = ""

        for key, value in NonEmptyAttributes.items():
            description += f"according{key} is {value}, "

        for key in EmptyAttributes.keys():
            nonDescription += f"lack condition {key}, "

        
        description = description.rstrip(", ")
        nonDescription = nonDescription.rstrip(", ")
        print(description)
        print(nonDescription)
        print(bookTimeToStr)
        print("May have to choose")

        i = 0
        output_set = set()

        for restaurant in found_restaurant:
            non_empty_items = {key: value for key, value in restaurant.items() if value is not None and value != ''}
            items_to_display = {
                key: value
                for key, value in non_empty_items.items()
                if value is not None and value != '' and key != 'roomID' and key != "isReserved"
            }
            # Build a description string
            description = ", ".join(f"{key} is {value}" for key, value in items_to_display.items())

            # Check whether the current restaurant information has been output
            if description not in output_set and i < 5:
                print(description)
                i += 1
                output_set.add(description)

        if i == 1:
            
            str1 = f"Are you want to book {description} at {bookTimeToStr}"
            print(str1)

        
        # for matched_intent in matched_intents:
        #     print(f"Matched Intent: {matched_intent['intent']}")
        #     print(f"Operation Result: {matched_intent['result']}")
    
    # temRestaurant.setReservedTime(bookTimeToStr)
    # temRestaurant.setIsReserved(1)
    # dbManager.insertRestaurant(temRestaurant)
    print(temRestaurant.toDict())
    
    print("Restaurant object is complete.")

    dbManager.closeConnection()

if __name__ == "__main__":
    run_main()

