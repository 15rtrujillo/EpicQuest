from plugins.functions import *
from plugins.triggers.talk_to_npc_trigger import TalkToNpcTrigger
from plugins.triggers.travel_to_room_trigger import TravelToRoomTrigger


class Default(TalkToNpcTrigger, TravelToRoomTrigger):
    def talk_to_npc(self) -> bool:
        mes(f"{get_npc().name.title()} does not appear interested in talking")
        pause()
        return True
    
    def travel_to_room(self) -> bool:
        travel()
        return True
