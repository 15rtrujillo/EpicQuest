from external.npc_def import NpcDef
from external.region_def import RegionDef


import input_output.file_utils as file_utils
import input_output.game_data_loader as game_data_loader


class World:
    def __init__(self):
        self.region_defs: dict[int, RegionDef] | None = None
        self.npc_defs: dict[int, NpcDef] | None = None

        self.load_region_defs()
        self.load_npc_defs()

    def load_region_defs(self):
        regions_directory = file_utils.get_regions_directory()
        region_files = file_utils.get_files_in_directory(regions_directory)
        for file_name in region_files:
            new_region_def = game_data_loader.load_region_file(file_name)
            if new_region_def is None:
                return
            self.region_defs[new_region_def.id] = new_region_def

    def load_npc_defs(self):
        npcs_directory = file_utils.get_npcs_directory()
        npc_files = file_utils.get_files_in_directory(npcs_directory)
        for file_name in npc_files:
            npc_def_list = game_data_loader.load_npc_file(file_name)
            if npc_def_list is None:
                return
            for new_npc_def in npc_def_list:
                self.npc_defs[new_npc_def.id] = new_npc_def
