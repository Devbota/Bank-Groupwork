# Manager for all transaction-related functions

# Import Account Classes
from AccountClass import Account

# Import Libraries
from DatabaseManager import DatabaseManager # Database Manager for logging in
import shortuuid # Unique Identifier generation
import hashlib # Hashing functions

class AccountManager():
  def __init__(self):
    self.__dm = DatabaseManager() # Initialises the Database Manager

  def Create_User(self, inpUsername:str, inpfName:str, inpLName:str, inpRole:str, inpPassword:str):
    # Creates a user object
    # UUID for the account should only be generated here, for security reasons
    inpUUID = shortuuid.uuid()

    # Salting and Hashing the password
    saltedPassword = inpPassword + inpUUID # The UUID of the account is the salt
    hashedPassword = hashlib.sha256(saltedPassword.encode('ascii')).hexdigest() # Hashing the salted password using SHA-256

    return Account(inpUUID, inpUsername, inpfName, inpLName, 0.00, inpRole, hashedPassword)

  def Login(self, inpUsername:str, inpPassword:str):
    # Checks to see if username and password combination is correct

    self.__dm.Manager_Start() # Start the Database Manager
    dbAccount = self.__dm.Get_Account_Username(inpUsername) # Gets the account associated with that username
    self.__dm.Manager_Stop() # Stop the Database Manager

    if dbAccount == False: # If the account does not exist
      return False

    dbUUID = dbAccount.Get_UUID() # Gets the UUID of the account

    # Salting and Hashing the input password
    saltedInpPassword = inpPassword + dbUUID
    hashedPassword = hashlib.sha256(saltedInpPassword.encode('ascii')).hexdigest()

    if hashedPassword == dbAccount.Get_Password():
      # Returns account if password is corrects
      return dbAccount
    else:
      return False
