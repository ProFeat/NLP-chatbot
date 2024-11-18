class Restaurant:
    def __init__(self):
        self._restaurantName = None
        self._expectedPrice = None
        self._roomName = None
        self._roomId = None
        self._sizes = None
        self._reservedTime = None
        self._isReserved = 0

    def getRestaurantName(self):
        return self._restaurantName

    def setRestaurantName(self, restaurantName):
        self._restaurantName = restaurantName

    def getRoomName(self):
        return self._roomName

    def setRoomName(self, roomName):
        self._roomName = roomName

    def getExpectedPrice(self):
        return self._expectedPrice

    def setExpectedPrice(self, expectedPrice):
        self._expectedPrice = expectedPrice

    def getRoomId(self):
        return self._roomId

    def getSizes(self):
        return self._sizes

    def setSizes(self, sizes):
        self._sizes = sizes

    def getIsReserved(self):
        return self._isReserved

    def setIsReserved(self, isReserved):
        self._isReserved = isReserved

    def getReservedTime(self):
        return self._reservedTime

    def setReservedTime(self, reservedTime):
        self._reservedTime = reservedTime

    def setFromDict(self, restaurantDict):
        self.setRestaurantName(restaurantDict.get("restaurantName", ""))
        self.setExpectedPrice(restaurantDict.get("expectedPrice", 0))
        self.setRoomName(restaurantDict.get("roomName", ""))
        self._roomId = restaurantDict.get("roomID", None)
        self.setSizes(restaurantDict.get("sizes"))
        self.setIsReserved(restaurantDict.get("isReserved", 0))
        self.setReservedTime(restaurantDict.get("reservedTime", ""))

    def toDict(self):
        return {
            "restaurantName": self._restaurantName,
            "expectedPrice": self._expectedPrice,
            "roomName": self._roomName,
            # "roomID": self._roomId,
            "sizes": self._sizes,
            "isReserved": self._isReserved,
            "reservedTime": self._reservedTime
        }
    
    def isComplete(self):
        # Check that all properties have met the condition
        return all([
            self._restaurantName and isinstance(self._restaurantName, str) and len(self._restaurantName) > 0,
            self.getExpectedPrice is not None,
            self._roomName and isinstance(self._roomName, str) and len(self._roomName) > 0,
            self._roomId is not None, 
            self._sizes is not None, 
            isinstance(self._isReserved, int) and self._isReserved in [0, 1],  
            # self._menu is not None and isinstance(self._menu, str), 
            self._reservedTime is not None and isinstance(self._reservedTime, str) 
            
        ])
    def setToNone(self):
        # Set all properties to None
        self._restaurantName = None
        self._expectedPrice = None
        self._roomName = None
        self._roomId = None
        self._sizes = None
        self._reservedTime = None
        self._isReserved = 0
        # self._menu = None