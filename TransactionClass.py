# Base class defining transaction objects 

class Transaction():
    def __init__(self, inpTransID:str, inpUserID:str, inpTransType:str, inpAmount:float):
        self.__transID = inpTransID # Unique Identifier for each transaction
        self.__userID = inpUserID # User ID of the user who made the transaction
        self.__transType = inpTransType # Type of transaction (Deposit or Withdrawal)
        self.__amount = inpAmount # Amount of the transaction

    # Get functions for all private variables

    def Get_Trans_ID(self):
        return self.__transID

    def Get_User_ID(self):
        return self.__userID

    def Get_Trans_Type(self):
        return self.__transType

    def Get_Amount(self):
        return self.__amount