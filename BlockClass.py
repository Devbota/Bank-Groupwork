# Base class defining block objects

# Import Libraries
import datetime # Date and Time functions

class Block():
    def __init__(self, inpIPAddress:str, inpDateTime:datetime.datetime):
        self.__ipAddress = inpIPAddress # IP Address of the user who is blocked
        self.__dateTime = inpDateTime # Date and Time of the block

    # Get functions for all private variables

    def Get_IP_Address(self):
        return self.__ipAddress

    def Get_DateTime(self) -> datetime.datetime: 
        # Returns date and time in an appropriate format
        return datetime.datetime.strptime(self.__dateTime, '%Y-%m-%d %H:%M:%S')