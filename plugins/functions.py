import external.npc_def as npc_def
from plugins.plugin_manager import PluginManager


def mes(*text: str):
    """Adds text to the current screen
    text: The message to be added"""
    for line in text:
        PluginManager.get_script_context().game.append_to_screen(line)


def pause():
    """Print the text \"Press ENTER to continue...\" to the screen"""
    PluginManager.get_script_context().game.pause()


def npc_say(*text: str, delay_ms: int = 25, end: str = "\n"):
    """Adds NPC dialog to the screen
    text: The dialog for the NPC
    delay_ms: For GUI interface, the time between each character getting added to the screen
    end: The character to append to the end of the NPC's dialog"""
    for line in text:
        PluginManager.get_script_context().game.typewriter(line, delay_ms, end)


def clear():
    """Clears the GUI screen
    Does nothing with the console"""
    PluginManager.get_script_context().game.clear_text()


def set_room(room_id: int):
    """Changes the interacting room to the one provided
    This does not relocate the player
    id: The ID of the room to set as interacting"""
    script_context = PluginManager.get_script_context()
    game = script_context.game
    if room_id in game.current_map.rooms.keys():
        new_room = game.current_map.rooms[room_id]
        script_context.interacting_room = new_room


def travel():
    """Moves the player to the interacting room"""
    script_context = PluginManager.get_script_context()
    player = script_context.interacting_player
    room = script_context.interacting_room
    game = script_context.game

    player.room = room.id
    game.display_screen(game.create_room_screen())


def get_npc() -> npc_def.Npc | None:
    """Get the NPC object the plugin is interacting with"""
    return PluginManager.get_script_context().interacting_npc
