import networkx as nx
from Safe_Cascade.util.class_function import update_dataclass
from Safe_Cascade.classes.power import *
import pypsa

def clean_network(lines, substations):
    graph = nx.Graph()
    [graph.add_node(_.name, pos=(_.location.x, _.location.y)) for _ in substations]
    [graph.add_edge(_.sub_1, _.sub_2) for _ in lines]
    isolated_subgraphs = nx.connected_components(graph)
    keep_substations = [_ for _ in isolated_subgraphs][0]
    lines = [_ for _ in lines if (_.sub_1 in keep_substations and _.sub_2 in keep_substations)]
    substations = [_ for _ in substations if _.name in keep_substations]
    return lines, substations


def check_connectivity(_substation, _line, _sub_out_status=1):
    graph = nx.Graph()
    [graph.add_node(_.name, pos=(_.location.x, _.location.y)) for _ in _substation if _.status == 0]
    [graph.add_edge(_.sub_1, _.sub_2) for _ in _line if _.status == 0]

    isolated_subgraphs = nx.connected_components(graph)
    subgraphs = sorted([_ for _ in isolated_subgraphs], key=len)
    keep_substations = subgraphs[-1]
    # update substation status
    [update_dataclass(_, status=_sub_out_status) for _ in _substation if
     _.name not in keep_substations and _.status == 0]
    [update_dataclass(_, status=_sub_out_status) for _ in _line if
     ((_.sub_1 not in keep_substations) or (_.sub_2 not in keep_substations)) and _.status == 0]

    ### add isolated substations to outage pool
    return keep_substations


def check_limit(_line: Line, current_flow: float):
    # threshold = 1.15
    return abs(current_flow) / (_line.mva_limit)


def keep_components(_subs, _lines, _trans, _buses, _gens, _loads):
    keep_substations = [_.name for _ in _subs if _.status == 0]
    # keep the connected network and elements
    # substations
    substations_keep = [_ for _ in _subs if _.status == 0]
    # buses
    buses_keep = [_ for _ in _buses if _.substation in keep_substations]
    _keep_buses = [_.name for _ in buses_keep]

    # generaters
    gens_keep = _gens
    # lines
    line_keep = [_ for _ in _lines if (_.sub_1 in keep_substations and _.sub_2 in keep_substations) and _.status == 0]
    # loads
    loads_keep = [_ for _ in _loads if _.substation in keep_substations]

    # transformers
    transformers_keep = [_ for _ in _trans if (_.bus1name in _keep_buses and _.bus2name in _keep_buses)]

    return substations_keep, line_keep, transformers_keep, buses_keep, gens_keep, loads_keep


def build_pypsa_network(_subs, _lines, _trans, _buses, _gens, _loads):
    _network = pypsa.Network()
    #add buses
    [_network.add('Bus', _.name, v_nom = _.voltage) for _ in _buses]
    #add lines
    [_network.add('Line', _l.name, bus0 = _l.bus1name, bus1 = _l.bus2name,  x=_l.x, r =_l.r) for _l in _lines ]
    #add loads
    [_network.add('Load', name= _.name, bus = _.bus_name,  p_set = _.p, q_set = _.q) for _ in _loads]
    #add generator
    [_network.add('Generator', name = _g.name, bus = _g.bus_name, p_set = _g.p_set, control = 'Slack') for _g in _gens if _g.status == 'Closed']
    #add transformer
    [_network.add('Transformer', name = _.name, bus0 = _.bus1name, bus1 = _.bus2name, x=_.x, r = _.r, s_nom = _.s_nom) for _ in _trans]
    return _network


def _pypsa_sim(_network, _lines):
    _network.lpf()
    flow_in_line = _network.lines_t.p0.transpose().reset_index()
    line_dict = {_.name:_ for _ in _lines}
    flow_in_line['rate'] = flow_in_line.apply(lambda x:check_limit(line_dict[x['index']], x['now']), axis = 1 )
    _failure_line = list(flow_in_line.query('rate > 1.15')['index'])
    _failure_line_id = list(set(_.split(':')[0] for _ in _failure_line))
    flow_in_line = flow_in_line.sort_values('rate', ascending=False)
    flow_in_line
    return _failure_line_id


def sim_in_pypsa(substations, lines, transformers, buses, generators, loads, failure_value= 2):
    _subs, _lines, _trans, _buses, _gens, _loads = keep_components(substations, lines, transformers, buses, generators, loads)
    failure_line = _pypsa_sim(build_pypsa_network(_subs, _lines, _trans, _buses, _gens, _loads), _lines)
    if len(failure_line)> 0:
        [update_dataclass(_, status = 2) for _ in lines if _.name in failure_line]
        _keep_substations = check_connectivity(substations, lines, failure_value)
    return failure_line
