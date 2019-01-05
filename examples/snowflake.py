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


# ObjectID class gets processed at runtime
class ObjectID(BitField):
    """
    Discord Object ID
    """

    timestamp = 42  # 42 bit custom epoch

    worker_id = 5  # 5 bit internal worker ID
    process_id = 5  # 5 bit process ID

    increment = 12  # 12 bit incrementing number


