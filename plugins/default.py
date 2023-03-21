from entity.npc import Npc
from entity.player import Player
from plugins.triggers.talk_to_npc_trigger import TalkToNpcTrigger
from plugins.triggers.travel_to_room_trigger import TravelToRoomTrigger
from room import Room


class Default(TalkToNpcTrigger, TravelToRoomTrigger):
    def talk_to_npc(self, player: Player, npc: Npc) -> bool:
        print()
        print(f"{npc.name.title()} does not appear interested in talking")
        print()
        return True
    
    def travel_to_room(self, player: Player, room: Room) -> bool:
        player.room = room.id
        return True
