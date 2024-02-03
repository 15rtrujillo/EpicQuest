from abc import ABC


class Screen(ABC):
    """The abstract base class for screens"""

    def __init__(self, text: str):
        """
        Create a new Screen
        :param str text: The text to display on the screen
        """
        self.text = text 


"""
class RoomScreen(Screen):
    \"""Screen that displays information about the current room\"""

    def __init__(self, current_map: MapDef, current_room: RoomDef, current_npcs: list[NpcDef]):
        \"""Create a screen to display the information about the current room
        current_map: The map the player is currently located in
        current_room: The room the player is currently located in
        current_npcs: The NPCs associated with the current Room\"""
        self.current_map = current_map
        self.current_room = current_room
        self.current_npcs = current_npcs

        # Create the text for this room
        text = current_room.description + "\n"

        # If there are NPCs, list them
        if len(self.current_npcs) > 0:
            text += "\n"
            for npc in self.current_npcs:
                text += f"You see {npc.name}\n"

        # If there are adjacent rooms, print those
        adj_rooms = self.get_adjacent_rooms()
        if len(adj_rooms) > 0:
            text += "\n"
            text += adj_rooms
        text += "\n"

        super().__init__(text)

    def get_adjacent_rooms(self) -> str:
        \"""Get a string with all the adjacent rooms\"""
        adj_rooms = ""
        for direction in word_lists.DIRECTIONS[:-2]:
            new_room_id = self.current_room.__dict__[direction]
            if new_room_id != -1:
                new_room = self.current_map.rooms[new_room_id]
                adj_rooms += f"To the {direction} you see {new_room.name}\n"

        return adj_rooms
"""
