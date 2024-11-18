import sqlite3

class RestaurantDatabaseManager:
    def __init__(self, databaseName="restaurantDatabase.db"):
        self.connection = sqlite3.connect(databaseName)
        self.createTables()

    def createTables(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS restaurants (
                    roomID INTEGER PRIMARY KEY,
                    restaurantName TEXT,
                    expectedPrice TEXT,
                    roomName TEXT,
                    isReserved INTEGER,
                    reservedTime TEXT,
                    sizes TEXT
                )
            ''')
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")
            raise

    def insertRestaurant(self, restaurant):
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO restaurants (restaurantName, expectedPrice, roomName, isReserved, reservedTime, sizes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                restaurant.getRestaurantName(),
                restaurant.getExpectedPrice(),
                restaurant.getRoomName(),
                restaurant.getIsReserved(),
                restaurant.getReservedTime(),
                restaurant.getSizes() if restaurant.getSizes() else None,
            ))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error inserting restaurant: {e}")
            raise

    # def getRestaurantByAttribute(self, attribute, value):
    #     cursor = self.connection.cursor()
    #     query = f'SELECT * FROM restaurants WHERE {attribute} = ?'
    #     cursor.execute(query, (value,))
    #     result = cursor.fetchone()
    #     if result:
    #         return {
    #             "roomId": result[0],
    #             "restaurantName": result[1],
    #             "expectedPrice": result[2],
    #             "roomName": result[3],
    #             "isReserved": result[4],
    #             "reservedTime": result[5],
    #             "menu": result[6],
    #             "sizes": result[7],
    #         }
    #     return None


    def getRestaurantByAttributes(self, restaurant):
        attributes = restaurant.toDict()
        cursor = self.connection.cursor()
    
        # Filter out properties with non-null values
        non_null_attributes = {key: value for key, value in attributes.items() if value is not None}
    
        # Build query criteria
        conditions = ' AND '.join([f'{attr} = ?' for attr in non_null_attributes])
        # print(conditions)
        query = f'SELECT * FROM restaurants WHERE {conditions}'
        # print(query)
        # print(non_null_attributes)
        try:
        # Try executing the query
            cursor.execute(query, tuple(non_null_attributes.values()))
            results = cursor.fetchall()

            # print("Results:", results) 

            restaurants = []
            for result in results:
                restaurant_info = {
                    "roomID": result[0],
                    "restaurantName": result[1],
                    "expectedPrice": result[2],
                    "roomName": result[3],
                    "isReserved": result[4],
                    "reservedTime": result[5],
                    "sizes": result[6],
                }
                restaurants.append(restaurant_info)
        
            return restaurants
        except Exception as e:
            # Catch an exception and handle it
            print(f"An error occurred: {e}")
            return None

    def getRestaurantById(self, restaurantID):
        try:
            cursor = self.connection.cursor()
            query = 'SELECT * FROM restaurants WHERE roomID = ?'
            cursor.execute(query, (restaurantID,))
            result = cursor.fetchone()
            if result:
                return {
                    "roomID": result[0],
                    "restaurantName": result[1],
                    "expectedPrice": result[2],
                    "roomName": result[3],
                    "isReserved": result[4],
                    "reservedTime": result[5],
                    "sizes": result[6],
                }
            return None
        except sqlite3.Error as e:
            print(f"Error getting restaurant by ID: {e}")
            raise

    def updateIsReservedByRoomID(self, restaurantID, isReserved):
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                UPDATE restaurants
                SET isReserved = ?
                WHERE roomID = ?
            ''', (isReserved, restaurantID))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error updating isReserved by roomID: {e}")
            raise

    def closeConnection(self):
        try:
            # Close the database connection
            if self.connection:
                self.connection.close()
        except sqlite3.Error as e:
            print(f"Error closing the database connection: {e}")
            raise
