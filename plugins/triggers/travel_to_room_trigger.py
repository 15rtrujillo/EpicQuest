from abc import ABC


class TravelToRoomTrigger(ABC):
    """Abstract class with methods to handle traveling to rooms"""

    def travel_to_room(self) -> bool:
        """
        The code to be run when attempting to travel to a new room
        :rtype: bool
        :return: This function should return True if the default action for this plugin should be blocked.
        """
        pass
