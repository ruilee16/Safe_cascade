from Safe_Cascade.util.read_inp import *
from Safe_Cascade.classes.stormwater import *


def load_swmm(path:str)-> dict:
    """
    load_swmm function read the SWMM .inp file and return the stormwater components as dictionary.
    :param path: the path to stormwater .inp file
    :return: a dictionary of the stormwater elements
    """
    tt = read_text_as_grp(path, "[")
    dt = {}
    for _ in tt:
        _dt = input_dt_prcr(_)
        if _dt:
            dt.update(_dt)
    return dt


def return_pumps(nodes_df:pd.DataFrame(),  pumps_df:pd.DataFrame(), links_curve_df:pd.DataFrame())->list:
    _nodes = list(nodes_df.apply(lambda x: _get_node(x), axis=1))
    _nodes_dict = {_.Node: (_.X_Coord, _.Y_Coord) for _ in _nodes}
    pumps = list(pumps_df.dropna().apply(lambda x: _get_pump(x), axis=1))
    _temp_curves_shp = _get_link_geomerty(links_curve_df)
    #update the pump shape
    [_get_link_geometry_from_nodes(_, _nodes_dict) for _ in pumps]
    [_get_link_geometry_from_curves(_, _temp_curves_shp, _nodes_dict) for _ in pumps]
    return pumps


def _get_node(df_value) -> Junction:
    _node_name = df_value['Node']
    return Junction(Node = _node_name, X_Coord = df_value["X-Coord"], Y_Coord = df_value["Y-Coord"])


def _get_link(df_value) -> Link:
    return Link(Name = df_value["Name"], FromNode = df_value["FromNode"], ToNode = df_value["ToNode"])


def _get_pump(df_value) -> Link:
    return Link(Name = df_value["Name"], FromNode = df_value["FromNode"], ToNode = df_value["ToNode"], isPump = True)


def _get_link_geometry_from_nodes(_link, nodes_dict) -> None:
    try:
        _link.geometry =  LineString([nodes_dict[_link.FromNode], nodes_dict[_link.ToNode]])
    except:
        pass


def _get_link_geometry_from_curves(_link, curve_dict, nodes_dict) -> None:
    try:
        if _link.Name in curve_dict:
            _temp = LineString([nodes_dict[_link.FromNode]]+curve_dict[_link.Name] + [nodes_dict[_link.ToNode]])
            _link.geometry = _temp
    except:
        pass


def _get_link_geomerty(vertices_df):
    _links_curve = vertices_df
    _links_curve['coord'] = list(zip(_links_curve['X-Coord'], _links_curve['Y-Coord']))
    curves_shp = _links_curve.groupby('Link').agg({'coord': list}).to_dict()['coord']
    curves_shp = {_: curves_shp[_] for _ in curves_shp.keys()}
    return curves_shp


