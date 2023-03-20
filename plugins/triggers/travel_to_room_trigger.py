from abc import ABC
from entity.player import Player
from room import Room


class TravelToRoomTrigger(ABC):
    """Abstract class with methods to handle traveling to rooms"""

    def travel_to_room(self, player: Player, room: Room) -> bool:
        """The code to be ran when attempting to travel to a new room
        player: The player
        room: The room being traveled to"""
        pass
