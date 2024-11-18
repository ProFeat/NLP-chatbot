from Restaurant import Restaurant  
import random

class RestaurantManager:
    def __init__(self, dbManager, numRestaurants=10):
        # to create RestaurantDatabaseManager instance
        self.dbManager = dbManager

        # Optional values for restaurant name, set menu, price and size
        self.restaurantNames = ["RestaurantA", "RestaurantB", "RestaurantC"]
        self.sizesOptions = ["Max", "Medium", "Small"]
        self.roomNameOptions = ["VIP room", "Standard room"]
        self.expectedPriceOptions = ["high price", "moderate price", "low price"]
        # Create the specified number of restaurants and insert the database
        self.createAndInsertRestaurants(numRestaurants)

    def createAndInsertRestaurants(self, numRestaurants):
        for i in range(1, numRestaurants + 1):
            restaurantName = random.choice(self.restaurantNames)
            expectedPrice = random.choice(self.expectedPriceOptions)
            roomName = random.choice(self.roomNameOptions)
            sizes = random.choice(self.sizesOptions)

            # Create a restaurant object
            # restaurant = Restaurant(restaurantName, expectedPrice, roomName)
            restaurant = Restaurant()
            restaurant.setRestaurantName(restaurantName)
            restaurant.setExpectedPrice(expectedPrice)
            restaurant.setRoomName(roomName)
            restaurant.setSizes(sizes)

            # Insert restaurant into database
            self.dbManager.insertRestaurant(restaurant)

        print(f"{numRestaurants} restaurants has been successfully inserted into the database.")

    def reserveRoom(self, restaurant):
        # Get the room ID
        roomId = restaurant.getRoomId()

        # Query the database for room information
        roomInfo = self.dbManager.getRestaurantById(roomId)

        # If the room does not exist, return the prompt message
        if not roomInfo:
            return False, "romm not find"

        # If the room is already booked, return the prompt message
        if roomInfo["isReserved"] == 1:
            return False, "room has been reserved"

        # Update the scheduled status
        self.dbManager.updateIsReservedByRoomID(roomId, 1)

        
        restaurant.setFromDict(roomInfo)
        return True, restaurant

    def findRestaurantByAttribute(self,restaurant):
        # Call the method of the database management class to get the restaurant information
        restaurant_info = self.dbManager.getRestaurantByAttributes(restaurant)

        if restaurant_info:
            
            # found_restaurant = Restaurant()
            # restaurant.setFromDict(restaurant_info)
            return restaurant_info
        else:
            
            # return False, "Room not find Input again"
            return None
        

