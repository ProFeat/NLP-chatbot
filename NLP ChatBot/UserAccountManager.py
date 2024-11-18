import re

class AuthenticationManager:
    def __init__(self, userDatabase):
        self.userDatabase = userDatabase

    def isValidEmail(self, email):
        # Detect mailbox format using simple regular expressions
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email) is not None

    def registerUser(self, user):
        # Check email format
        if not self.isValidEmail(user.getEmail()):
            return False, "Invalid email format"

        # check email exit
        emailExists = self.userDatabase.checkEmailExists(user.getEmail())
        if emailExists:
            # email exit return
            return False, "Email already exists"

        # register insertuer
        self.userDatabase.insertUser(user)
        return True, "User registered successfully"


    def loginUser(self, user):
        # check email format
        if not self.isValidEmail(user.getEmail()):
            return False, "Invalid email format", None

        # check email exit
        emailExists = self.userDatabase.checkEmailExists(user.getEmail())
        if not emailExists:
            # not exit return
            return False, "Email does not exist", None

        # load date from dateabase
        userData = self.userDatabase.loadUserByEmail(user.getEmail())
        if userData:
            # verify passwoef
            if userData['password'] == user.getPassword():
                # return load user date
                return True, "Login successful", userData
            else:
                # password wrong
                return False, "Incorrect password", None
        else:
            # not find
            return False, "User data not found", None

    def queryUserInfo(self, email):
        # query user
        userInfo = self.userDatabase.loadUserByEmail(email)
        if userInfo:
            return True, "Query user information successful", userInfo
        else:
            # not find
            return False, "Query user information failed, user does not exist", None

    def updateUserInfo(self, user):
        # update
        try:
            # format email
            if not self.isValidEmail(user.getEmail()):
                return False, "Invalid email format for updating user information"

            self.userDatabase.updateUser(user)
            return True, "Update user information successful"
        except Exception as e:
            return False, f"Update user information failed: {e}"
