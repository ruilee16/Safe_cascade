import pandas as pd
import geopandas as gpd
import rasterio
from rasterstats import zonal_stats
from typing import List
from Safe_Cascade.util.class_function import update_dataclass
import random


def get_wind_at_line(wind_raster: str, line_list:List, line_crs, geometry = 'location'):
    wind_crs = rasterio.open(wind_raster).crs
    line_vector = gpd.GeoDataFrame(pd.DataFrame(line_list), geometry = geometry, crs = line_crs )
    line_vector = line_vector.to_crs(wind_crs)
    stats = zonal_stats(line_vector, wind_raster, stats="max")
    [update_dataclass(line_list[_], wind_speed = stats[_]['max']) for _ in range(len(stats))]


def wind_fragility_curve(speed:int)->List:
    if speed < 67: #67mph (30m/s)
        _failure_prb = 0.01/67*speed
    elif speed >=112:
        _failure_prb = 0.99
    else:
        _failure_prb = 0.0218*speed-1.45
    return [1-_failure_prb, _failure_prb]


def random_fail(line:List, failure_ratio=0):
    #reset line status
    [update_dataclass(_, status = 0) for _ in line]
    values = [0, 1] # 0: line survive. 1: line fail. 2: line fail after pyPSA
    if failure_ratio>0:
        [update_dataclass(_, status = 1) for _ in line if random.choices(values, [1-failure_ratio, failure_ratio])[0] == 1 and _.voltage == 69]
    else:
        [update_dataclass(_, status = 1) for _ in line if random.choices(values, wind_fragility_curve(_.wind_speed))[0] == 1 and _.voltage == 69]
    new_line = [_ for _ in line if _.status == 0]
    return new_line
