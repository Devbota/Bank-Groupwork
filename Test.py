# Import Managers
from AccountManager import AccountManager
from DatabaseManager import DatabaseManager
from TransactionManager import TransactionManager

# Import Libraries
import re # Regular Expressions for password validation

# Initialise Managers
dm = DatabaseManager()
am = AccountManager()
tm = TransactionManager()

# Initialise Users

user1 = am.Create_User("JohnSmith1", "John", "Smith", "user", "Passw0rd123")
admin1 = am.Create_User("AdminAccount", "Admin", "Account", "admin", "12345!qQ")

dm.Manager_Start()
dbAccount = dm.Add_Account(user1)
dbAccount = dm.Add_Account(admin1)
dm.Manager_Stop()