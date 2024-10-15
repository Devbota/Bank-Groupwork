# Manager for all log-related functions

# Import Log Classes
from LogClass import LogEntry

# Import Libraries
import shortuuid # Unique Identifier generation
import datetime # Date and Time functions

class LogManager():
    def __init__(self):
        pass

    def Create_Log(self, inpUser1ID:str, inpUser2ID:str, inpEventType:str, inpIPAddress:str):
        # UUID and date/time for the log should only be generated here, for security reasons
        inpUUID = shortuuid.uuid()
        inpDateTime = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        return LogEntry(inpUUID, inpUser1ID, inpUser2ID, inpEventType, inpIPAddress, inpDateTime)