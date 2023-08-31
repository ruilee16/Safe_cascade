import geopandas as gpd
import pandas as pd


def dependant_power_sub(power_service_region, target_compoent):
    target_compoent['geometry'] = target_compoent.centroid
    _result = target_compoent.to_crs(power_service_region.crs).sjoin(power_service_region)
    return _result


def pump_sub_dependency(power_service_region, pumps_list, pumps_crs):
    pumps_gdf = gpd.GeoDataFrame(pd.DataFrame(pumps_list), crs=pumps_crs)
    pump_substation = dependant_power_sub(power_service_region, pumps_gdf)
    _pumps_dict = {_.Name:_ for _ in pumps_list}
    pump_substation.apply(lambda x: _pumps_dict[x['Name']].set_substation_id(x['SubName']), axis = 1)