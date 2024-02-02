from external.region_def import RegionDef


import model.world.room as room


class Region:
    def __init__(self, region_def: RegionDef):
        self.id: int = region_def.id
        self.region_def: RegionDef = region_def
        self.starting_room: room.Room | None = None
