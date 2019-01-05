"""
Example Usage: Snowflake IDs
============================

Discord is one of many platforms to use Snowflake IDs.

Object IDs on Discord are 64 bit integers that get split up into several numbers to encode metadata about the object.
The first 42 bits represent a custom epoch, 10 bits represent worker and process IDs, and the last 12 bits are simply
incremented.

https://discordapp.com/developers/docs/reference
"""

import sys

sys.path.insert(0, "./../")

from colorguard import BitField
from datetime import datetime


# ObjectID class gets processed at runtime
class ObjectID(BitField):
    """
    Discord Object ID
    """

    timestamp = 42  # 42 bit custom epoch

    worker_id = 5  # 5 bit internal worker ID
    process_id = 5  # 5 bit process ID

    increment = 12  # 12 bit incrementing number

    @property
    def created_at(self):
        # custom property to convert timestamp to datetime

        # attributes are accessed through indexing
        epoch = self["timestamp"] + 1420070400000  # discord epoch

        return datetime.utcfromtimestamp(epoch / 1000)

    @created_at.setter
    def created_at(self, value):
        # change timestamp by converting back to discord epoch

        self["timestamp"] = int(value.timestamp() * 1000 - 1420070400000)  # MUST be converted to int!


# example ID from 2016/4/30
obj = ObjectID.from_bits(175928847299117063)

print(obj)
# > ObjectID(timestamp=41944705796, worker_id=1, process_id=0, increment=7)


# Use property we defined to get datetime
print(obj.created_at)
# > datetime.datetime(2016, 4, 30, 11, 18, 25, 796000)

# Awesome! Now let's try changing it with the setter
obj.created_at = datetime(2092, 3, 28)
print(obj)
# > ObjectID(timestamp=2437444800000, worker_id=1, process_id=0, increment=7)
