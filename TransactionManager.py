# Manager for all transaction-related functions

# Import Transaction Classes
from TransactionClass import Transaction

# Import Libraries
import shortuuid # Unique Identifier generation

class TransactionManager():
    def __init__(self):
        pass

    def Create_Transaction(self, inpUserID:str, inpTransType:str, inpAmount:float):
        # UUID for the transaction should only be generated here, for security reasons
        inpUUID = shortuuid.uuid()

        return Transaction(inpUUID, inpUserID, inpTransType, inpAmount)