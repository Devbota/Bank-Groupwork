# Manager for all Block-related functions

# Import Block Classes
from BlockClass import Block

# Import Libraries
import datetime # Date and Time functions

class BlockManager():
    def __init__(self):
        pass

    def Create_Block(self, inpIPAddress:str):
        # Date for the block should only be generated here, for security reasons

        # Formatting date and time for the block
        inpDateTime = datetime.datetime.now() + datetime.timedelta(days=1)
        inpDateTime = inpDateTime.strftime('%Y-%m-%d %H:%M:%S')
        return Block(inpIPAddress, inpDateTime)
    
    def Block_Expired(self, block:Block):
        # Check if the block has expired, returns boolean value

        if block.Get_DateTime() < datetime.datetime.now():
            return True
        else:
            return False