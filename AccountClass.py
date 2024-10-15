# Base class defining Account objects

class Account():
    def __init__(self, inpUUID:str, inpUsername:str, inpfName:str, inpLName:str, inpBalance:float, inpRole:str, inpPassword:str):
        self.__UUID = inpUUID # Unique Identifier for each account
        self.__Username = inpUsername # Username of the account [UNIQUE]
        self.__fName = inpfName # First Name of the account holder
        self.__lName = inpLName # Last Name of the account holder
        self.__balance = inpBalance # Balance of the account
        self.__Role = inpRole # Role of the account (Admin or User)
        self.__Password = inpPassword # Salted + HashedPassword of the account

    # Get functions for all private variables

    def Get_UUID(self):
        return self.__UUID

    def Get_Username(self):
        return self.__Username

    def Get_fName(self):
        return self.__fName

    def Get_lName(self):
        return self.__lName

    def Get_Balance(self):
        return self.__balance

    def Get_Role(self):
        return self.__Role

    def Get_Password(self):
        return self.__Password
    
    # Set functions for all private variables
    
    def Set_Balance(self, inpBalance):
        self.__balance = inpBalance # Set the balance of the account
