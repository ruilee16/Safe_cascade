import pandas as pd
from Safe_Cascade.classes.power import *
from Safe_Cascade.util.class_function import update_dataclass

def get_bus(bus_list: List, bus_num: int):
    _bus_dict = {_.bus_num:_ for _ in bus_list}
    return _bus_dict[bus_num]

def get_sub(sub_list: List, sub_name: int):
    _sub_dict = {_.name:_ for _ in sub_list}
    return _sub_dict[sub_name]

def get_substations(url):
    substations_df = pd.read_csv(url)
    substations = substations_df.apply(lambda x: SubStation(name=x['SubName'],
                                                            location=Point(x['Longitude'], x['Latitude']),
                                                            subid=x['SubID']), axis=1).to_list()
    return substations


def get_buses(url):
    buses_df = pd.read_csv(url)
    buses = buses_df.apply(lambda x: Bus(name=x['BusName'],
                                         bus_num=x['BusNum'],
                                         voltage=x['BusNomVolt'],
                                         substation=x['BusName'][:-len(str(x['BusNomVolt']))]), axis=1).to_list()

    return buses


def get_transformers(url, buses_list):
    transformers_df = pd.read_csv(url)
    transformers = transformers_df.apply(lambda row: Transformer(
        name="{}-{}-txfmr".format(row['BusNum'], row['BusNum:1']),
        bus1name=get_bus(buses_list, row['BusNum']).name,
        bus2name=get_bus(buses_list, row['BusNum:1']).name,
        substation=get_bus(buses_list, row['BusNum:1']).substation,
        r=row['LineR:1'],
        x=row['LineX:1'],
        s_nom=row['XFMVABase']), axis=1).to_list()
    return transformers


def update_names(data_list):
    #transformers and transmission lines need this step
    transformers_name = {}
    for _ in data_list:
        _name = _.name
        if _name in transformers_name:
            transformers_name[_name] = transformers_name[_name] + 1
        else:
            transformers_name[_name] = 1
        update_dataclass(_, name=f'{_name}-{transformers_name[_name]}')


def get_transmissionlines(url, buses, substations):
    lines_df =  pd.read_csv(url)
    lines = lines_df.apply(lambda row: Line(name="Line-{}-{}".format(row['BusNum'], row['BusNum:1']),
                                            bus1name=get_bus(buses, row['BusNum']).name,
                                            bus2name=get_bus(buses, row['BusNum:1']).name,
                                            sub_1=get_sub(substations, get_bus(buses, row['BusNum']).substation).name,
                                            sub_2=get_sub(substations, get_bus(buses, row['BusNum:1']).substation).name,
                                            r=row['LineR'],
                                            x=row['LineX'],
                                            mva_limit=row['LineAMVA'],
                                            voltage=get_bus(buses, row['BusNum']).voltage,
                                            location=LineString([get_sub(substations, get_bus(buses, row[
                                                'BusNum']).substation).location,
                                                                 get_sub(substations, get_bus(buses, row[
                                                                     'BusNum:1']).substation).location])),
                           axis=1).to_list()
    return lines


def get_generators(url, buses):
    gen_df = pd.read_csv(url)
    generators = gen_df.apply(lambda x: Generator(name=f"{str(x['BusNum'])}-{str(x['GenID'])}",
                                                  bus_num=x['BusNum'],
                                                  bus_name=get_bus(buses, x['BusNum']).name,
                                                  gen_id=x['GenID'],
                                                  v_pu=x['GenVoltSet'],
                                                  p_set=x['GenMWSetPoint'],
                                                  status=x['GenStatus']), axis=1).to_list()
    return generators


def get_loads(url, buses):
    loads_df = pd.read_csv(url)
    loads = loads_df.apply(lambda x: Load(name="{}-Load".format(x['BusNum']),
                                          p=x['LoadSMW'],
                                          q=x['LoadSMVR'],
                                          substation=get_bus(buses, x['BusNum']).substation,
                                          bus_name=get_bus(buses, x['BusNum']).name), axis=1).to_list()
    return loads



