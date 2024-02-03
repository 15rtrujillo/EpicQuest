from external.region_def import RegionDef


import model.world.room as room


class Region:
    """A collection of Rooms"""

    def __init__(self, region_def: RegionDef):
        """
        Create a new region based on a region definition
        :param RegionDef region_def: The region definition to base this region on
        """
        self.id = region_def.id
        self.region_def = region_def
        self.starting_room: room.Room | None = None
