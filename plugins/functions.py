from plugins.plugin_manager import PluginManager


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
