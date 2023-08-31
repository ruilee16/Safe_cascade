from dataclasses import dataclass, field
from shapely.geometry import Point, LineString
from typing import List


@dataclass()
class SubStation:
    name: str = field(compare=False)
    location: Point = field(default=None)
    # voltage: List[int] = field(default_factory = list)
    # line_number: str = field(default = 0)
    # load_kwh: float = field(default = 0)
    # is_generator: bool = field(default = False)
    # check: bool = field(default=False)
    subid: int = field(default=None)
    status: int = field(default=1)


@dataclass
class Bus:
    name: str = field(compare=True)
    bus_num: int = field(default=None)
    substation: str = field(default=None)
    voltage: List[int] = field(default_factory=list)
    is_load: bool = field(default=False)
    v_mag_pu_set: float = field(default=0)


@dataclass
class Generator:
    name: str = field(compare=True)
    bus_num: int = field(default=None)
    bus_name: str = field(default=None)
    gen_id: int = field(default=None)
    v_pu: float = field(default=0)
    p_set: float = field(default=0)
    status: str = field(default=False)


@dataclass
class Line:
    name: str = field(default=None)
    bus1name: str = field(default=None)
    bus2name: str = field(default=None)
    sub_1: str = field(default=None)
    sub_2: str = field(default=None)
    r: float = field(default=None)
    x: float = field(default=None)
    mva_limit: float = field(default=0)
    voltage: int = field(default=0)
    location: LineString = field(default=None)
    wind_speed: int = field(default=0)
    status: int = field(default=1)


@dataclass
class Load:
    name: str = field(default=None)
    bus_name: int = field(default=None)
    substation: str = field(default=None)
    p: float = field(default=None)
    q: float = field(default=None)


@dataclass
class Transformer:
    name: str = field(default=None)
    bus1name: str = field(default=None)
    bus2name: str = field(default=None)
    substation: str = field(default=None)
    r: float = field(default=None)
    x: float = field(default=None)
    s_nom: float = field(default=None)
