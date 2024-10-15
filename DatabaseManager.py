# This file acts as a data-link layer, so that only this program interacts with the database. 
# This is done to prevent any unauthorized access to the database, and helps in maintaining the integrity of the data.

# If the program is to be scaled: 
# This can be easily modified to include more functions, or this program can be split into multiple files.
# The other files would be separated by the classes they deal with in a format similar to "BLLs"

# Import established Classes
from AccountClass import Account
from TransactionClass import Transaction
from LogClass import LogEntry
from BlockClass import Block

# Import Libraries
import sqlite3 #Enables database functions

class DatabaseManager():
    def __init__(self):
        pass


    # The following functions are used to start and stop the database connection
    # This is done to:
    #    Prevent multiple connections to the database
    #    Prevent unauthorized access to the database
    #    Prevent data corruption
    #    Prevent memory leaks
    #    etc.


    def Manager_Start(self):
        self.__connection = sqlite3.connect("SDSDB.db")
        self.__cursor = self.__connection.cursor()

    def Manager_Stop(self):
        self.__connection.close()


    # The following functions are used to interact with the database
    # The functions are separated by the class they interact with
    # They are ordered by the following: Add, Remove, Edit, Get


    def Add_Account(self, user:Account):
        # Adds an account to the database

        query = f"""
            INSERT INTO Accounts (uuid, role, username, password, fName, lName, balance)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        
        # Every "?" is a placeholder for a value to be inserted

        self.__cursor.execute(query, (user.Get_UUID(), user.Get_Role(), user.Get_Username(), user.Get_Password(), user.Get_fName(), user.Get_lName(), user.Get_Balance(), ))
        self.__connection.commit()

    def Remove_Account(self, user:Account):
        # Removes an account from the database

        query = """
            DELETE FROM Accounts WHERE uuid = ?
        """

        self.__cursor.execute(query, (user.Get_UUID(),))
        self.__connection.commit()

    def Edit_Balance(self, user:Account, attributeVal:str):
        # Edits the balance of an account

        query = """
            UPDATE Accounts SET balance = ? WHERE uuid = ?
            """
        
        self.__cursor.execute(query, (attributeVal, user.Get_UUID(),))
        self.__connection.commit()

    def Get_Account_UUID(self, uuid:str):
        # Gets an account from the database using the UUID

        query = """
            SELECT * FROM Accounts WHERE uuid = ?
        """

        self.__cursor.execute(query, (uuid,))

        try:
            account = self.__cursor.fetchall()[0]
            return Account(account[0], account[2], account[4], account[5], account[6], account[1], account[3])
        except IndexError:
            return False

    def Get_Account_Username(self, username: str):
        # Gets an account from the database using the username

        query = """
            SELECT * FROM Accounts WHERE username = ?
        """
        self.__cursor.execute(query, (username,))

        try:
            account = self.__cursor.fetchall()[0]
            return Account(account[0], account[2], account[4], account[5], account[6], account[1], account[3])
        except IndexError:
            return False
        
    def Get_All_Usernames(self):
        # Gets all usernames from the database

        query = """
            SELECT username FROM Accounts
        """

        usernames = self.__cursor.execute(query).fetchall()
        output = []

        for item in usernames:
            output.append(item[0])

        return output

    def Add_Transaction(self, transaction:Transaction):
        # Adds a transaction to the database

        query = """
            INSERT INTO Transactions (transID, userID, transType, amount)
            VALUES (?, ?, ?, ?)
        """

        self.__cursor.execute(query, (transaction.Get_Trans_ID(), transaction.Get_User_ID(), transaction.Get_Trans_Type(), transaction.Get_Amount(), ))
        self.__connection.commit()

    def Get_Transaction_ID(self, transID:str):
        # Gets a transaction from the database using the transaction ID

        query = """
            SELECT * FROM Transactions WHERE transID = ?
        """

        transaction = self.__cursor.execute(query, (transID,)).fetchall()[0]

        return Transaction(transaction[0], transaction[1], transaction[2], transaction[3])

    def Get_Transaction_UserID(self, userID:str):
        # Gets all transactions from the database using the user ID

        query = """
            SELECT * FROM Transactions WHERE userID = ?
        """

        transaction = self.__cursor.execute(query, (userID, )).fetchall()

        transList = []

        for item in transaction:
            transList.append(Transaction(item[0], item[1], item[2], item[3]))

        transList.reverse()

        return transList

    def Add_Log_Entry(self, event:LogEntry):
        # Adds a log entry to the database

        query = """
            INSERT INTO Log (eventID, user1ID, user2ID, eventType, ipAddress, dateTime)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        
        self.__cursor.execute(query, (event.Get_Event_ID(),
                                      event.Get_User1_ID(),
                                      event.Get_User2_ID(),
                                      event.Get_Event_Type(),
                                      event.Get_IP_Address(),
                                      event.Get_Date_Time(),
                                      ))
        self.__connection.commit()

    def Get_All_Logs(self):
        # Gets all log entries from the database

        query = """
            SELECT * FROM Log
        """

        entry = self.__cursor.execute(query).fetchall()

        logList = []
        
        for log in entry:
            logList.append(LogEntry(log[0], log[1], log[2], log[3], log[4], log[5]))

        logList.reverse()

        return logList

    def Get_Log_Entry_EventID(self, eventID:str):
        # Gets a log entry from the database using the event ID

        query = """
            SELECT * FROM Log WHERE eventID = ?
        """

        entry = self.__cursor.execute(query, (eventID, )).fetchall()[0]

        return LogEntry(entry[0], entry[1], entry[2], entry[3], entry[4], entry[5])

    def Get_Log_Entry_User1ID(self, user1ID:str):
        # Gets all log entries from the database using the user1 ID
        query = f"""
            SELECT * FROM Log WHERE user1ID = ?
        """

        entry = self.__cursor.execute(query, (user1ID, )).fetchall()
        logList = []

        for item in entry:
            logList.append(LogEntry(item[0], item[1], item[2], item[3], item[4], item[5]))

        logList.reverse()

        return logList

    def Get_Log_Entry_User2ID(self, user2ID:str):
        # Gets all log entries from the database using the user2 ID
        query = f"""
            SELECT * FROM Log WHERE user2ID = ?
        """

        entry = self.__cursor.execute(query, (user2ID, )).fetchall()
        logList = []

        for item in entry:
            logList.append(LogEntry(item[0], item[1], item[2], item[3], item[4], item[5]))

        logList.reverse()

        return logList

    def Get_Log_Entry_IPAddress(self, ipAddress:str):
        # Gets all log entries from the database using the IP Address
        query = """
            SELECT * FROM Log WHERE ipAddress = ?
        """

        entry = self.__cursor.execute(query, (ipAddress, )).fetchall()
        logList = []

        for item in entry:
            logList.append(LogEntry(item[0], item[1], item[2], item[3], item[4], item[5]))

        logList.reverse()

        return logList

    def Add_Block(self, block:Block):
        # Adds a block to the database

        query = """
            INSERT INTO Blocked_IPs (ipAddress, dateTime)
            VALUES (?, ?)
        """
        
        self.__cursor.execute(query, (block.Get_IP_Address(), block.Get_DateTime(), ))
        self.__connection.commit()

    def Remove_Block(self, block:Block):
        # Removes a block from the database

        query = """
            DELETE FROM Blocked_IPs WHERE ipAddress = ?
        """

        self.__cursor.execute(query, (block.Get_IP_Address(), ))
        self.__connection.commit()

    def Get_Block_Entry_IPAddress(self, ipAddress:str):
        # Gets a block from the database using the IP Address

        query = """
            SELECT * FROM Blocked_IPs WHERE ipAddress = ?
        """

        try:
            block = self.__cursor.execute(query, (ipAddress, )).fetchall()[0]
            return Block(block[0], block[1])
        except:
            return False