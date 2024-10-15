# Base class defining transaction objects 

# Import Libraries
import datetime # Date and Time functions

class LogEntry():
    def __init__(self, inpEventID:str, inpUser1ID:str, inpUser2ID:str, inpEventType:str, inpIPAddress:str, inpDateTime:datetime.datetime):
        # datetime.datetime is an complex data type that stores the date and time

        self.__eventID = inpEventID # Unique Identifier for each event
        self.__user1ID = inpUser1ID # User ID of the user who initiated the event
        self.__user2ID = inpUser2ID # User ID of the user who was affected by the event
        self.__eventType = inpEventType # Type of event (Login, Logout, Deposit, Withdrawal, etc.)
        self.__ipAddress = inpIPAddress # IP Address of the user who initiated the event
        self.__dateTime = inpDateTime # Date and Time of the event

    # Get functions for all private variables

    def Get_Event_ID(self):
        return self.__eventID

    def Get_User1_ID(self):
        return self.__user1ID

    def Get_User2_ID(self):
        return self.__user2ID

    def Get_Event_Type(self):
        return self.__eventType
    
    def Get_IP_Address(self):
        return self.__ipAddress
    
    def Get_Date_Time(self):
        return self.__dateTime