from plugins.functions import *
from plugins.triggers.talk_to_npc_trigger import  TalkToNpcTrigger


class MysteriousFigure(TalkToNpcTrigger):
    def talk_to_npc(self) -> bool:
        if get_npc().id != 0:
            return False
        mes("This is a test")
        npc_say("Hello there...",
                "Welcome to Epic Quest",
                "This is a test of the dialog system lol")
        pause()
        return True
