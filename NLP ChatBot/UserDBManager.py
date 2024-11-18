import sqlite3

class UserDatabase:
    def __init__(self, dbPath='userDatabase.db'):
        # Initialize UserDatabase using the default database path
        self.dbPath = dbPath
        # Connect to the database and create the user table
        self.connection = self.connectToDatabase()
        self.createUserTable()

    def connectToDatabase(self):
        try:
            # Connect to the SQLite database
            connection = sqlite3.connect(self.dbPath)
            return connection
        except sqlite3.Error as e:
            # Handle connection errors
            print(f"Error connecting to the database: {e}")
            raise

    def createUserTable(self):
        try:
            # Create the 'users' table if it doesn't exist
            cursor = self.connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    userId INTEGER PRIMARY KEY AUTOINCREMENT,
                    userName TEXT,
                    email TEXT,
                    password TEXT,
                    logoutTime TEXT
                )
            ''')
            self.connection.commit()
        except sqlite3.Error as e:
            # Handle errors when creating the user table
            print(f"Error creating the user table: {e}")
            raise

    def insertUser(self, user):
        try:
            # Insert a new user into the 'users' table
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO users (userName, email, password, logoutTime)
                VALUES (?, ?, ?, ?)
            ''', (user.getUserName(), user.getEmail(), user.getPassword(), user.getLogoutTime()))
            self.connection.commit()
        except sqlite3.Error as e:
            # Handle errors when inserting user data
            print(f"Error inserting user data: {e}")
            raise

    def updateUser(self, user):
        try:
            # Construct the SQL statement
            sqlStatement = '''
                UPDATE users
                SET userName = ?, email = ?, password = ?, logoutTime = ?
                WHERE userId = ?
            '''
            
            # Execute the SQL statement
            cursor = self.connection.cursor()
            cursor.execute(sqlStatement, (user.getUserName(), user.getEmail(), user.getPassword(), user.getLogoutTime(), user.getUserId()))
            
            # Commit the changes
            self.connection.commit()
        except sqlite3.Error as e:
            # Handle errors when updating user information
            print(f"Error updating user information: {e}")
            raise

    def loadUserByEmail(self, email):
        try:
            # Load user data from the 'users' table by email
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            row = cursor.fetchone()
            if row:
                # 将元组转换为字典
                user_data = {
                    'userId': row[0],
                    'userName': row[1],
                    'email': row[2],
                    'password': row[3],
                    'logoutTime': row[4]
                }
                return user_data
            else:
                # 用户不存在，明确返回 None
                return None
        except sqlite3.Error as e:
            # Handle errors when loading user data from the database
            print(f"Error loading user information from the database: {e}")
            raise

    def checkEmailExists(self, email):
        try:
            # Check if the email exists
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            row = cursor.fetchone()
            if row:
                # Email exists
                return True
            else:
                # Email is available
                return False
        except sqlite3.Error as e:
            # Handle errors when checking if the email exists
            errorMessage = f"Error checking if the email exists: {e}"
            print(errorMessage)
            return None

    def closeConnection(self):
        try:
            # Close the database connection
            if self.connection:
                self.connection.close()
        except sqlite3.Error as e:
            # Handle errors when closing the database connection
            print(f"Error closing the database connection: {e}")
            raise
