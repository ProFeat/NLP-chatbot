class User:
    def __init__(self, userId, userName, email, password, logoutTime):
        self.userId = userId
        self.userName = userName
        self.email = email
        self.password = password
        self.logoutTime = logoutTime

    def getUserId(self):
        return self.userId

    def getUserName(self):
        return self.userName

    def getEmail(self):
        return self.email

    def getPassword(self):
        return self.password

    def getLogoutTime(self):
        return self.logoutTime
    
    def setUserEmail(self, email):
        self.email = email

    def setUserName(self, userName):
        self.userName = userName

    def setPassword(self, password):
        self.password = password

    def setLogoutTime(self, logoutTime):
        self.logoutTime = logoutTime

    def setFromDict(self, userDict):
        self.userId = userDict.get('userId')
        self.userName = userDict.get('userName')
        self.email = userDict.get('email')
        self.password = userDict.get('password')
        self.logoutTime = userDict.get('logoutTime')
        
    def checkPassword(self, password):
        return self.password == password

    def __str__(self):
        return f"User ID: {self.userId}, Username: {self.userName}, Email: {self.email}, Logout Time: {self.logoutTime}"
