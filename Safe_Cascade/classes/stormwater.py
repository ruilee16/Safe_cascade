import dataclasses
from shapely.geometry import LineString, MultiLineString


@dataclasses.dataclass
class Junction():
    Node: str = dataclasses.field(default=None)
    X_Coord: float = dataclasses.field(default=None)
    Y_Coord: float = dataclasses.field(default=None)
    Elevation: int = dataclasses.field(default=None)
    MaxDepth: float = dataclasses.field(default=None)
    InitDepth: float = dataclasses.field(default=None)
    SurDepth: float = dataclasses.field(default=None)
    Aponded: float = dataclasses.field(default=None)


@dataclasses.dataclass
class Link():
    Name: str = dataclasses.field(default=None)
    FromNode: str = dataclasses.field(default=None)
    ToNode: str = dataclasses.field(default=None)
    Length: float = dataclasses.field(default=None)
    Roughness: float = dataclasses.field(default=None)
    InOffset: float = dataclasses.field(default=None)
    OutOffset: float = dataclasses.field(default=None)
    InitFlow: float = dataclasses.field(default=None)
    MaxFlow: float = dataclasses.field(default=None)
    substation_id: str = dataclasses.field(default=None)
    isPump: bool = dataclasses.field(default=None)
    geometry: LineString = dataclasses.field(default=None)

    def set_nodes(self, FromNode, ToNode):
        self.FromNode = FromNode
        self.ToNode = ToNode

    def set_pump(self, isPump):
        self.isPump = isPump

    def set_substation_id(self, substation_id):
        self.substation_id = substation_id


@dataclasses.dataclass
class Node:
    nodeid: int = dataclasses.field(default=None)
    x: float = dataclasses.field(default=None)
    y: float = dataclasses.field(default=None)
    PDW_region: str = dataclasses.field(default=None)

    def set_coordinates(self, x, y):
        self.x = x
        self.y = y

    def set_power_region(self, PDW_region):
        self.PDW_region = PDW_region