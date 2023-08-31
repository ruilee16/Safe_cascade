import re
import io
import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO
import pandas as pd


def _get_groups(seq: str, group_by: str):
    """
    Split the .inp/.aux file into different groups based on the document section seperator
    :param seq: intake string of the document
    :param group_by: seperater
    :return:
    """
    data = []
    for line in seq:
        if line.startswith(group_by):
            if data:
                yield data
                data = []
        data.append(line)
    if data:
        yield data


def _blk_prcr(blk: str):
    """
    input t: string of the record
    using the .inp/.aux format
    """
    _temp_ls = blk.strip().split('\n')
    _col_sep = _temp_ls[2].split()
    del _temp_ls[2]
    _col_loc = [len(_) for _ in _col_sep]
    _t_loc = [sum(_col_loc[:_])+_ for _ in range(len(_col_loc)+1)]
    _t_set = list(zip(_t_loc[0:-1], _t_loc[1:]))
    _temp_rec = []
    for _row in _temp_ls[1:]:
        _row_rec = []
        for _rec in range(len(_t_set)):
            if _rec == len(_t_set)-1:
                _row_rec.append(_row[_t_set[_rec][0]:].strip())
            else:
                _row_rec.append(_row[_t_set[_rec][0]:_t_set[_rec][-1]].strip())
        _temp_rec.append(' '.join(_row_rec))
    return re.search(r"\[([A-Za-z0-9_]+)\]", _temp_ls[0]).group(1),'\n'.join(_temp_rec).replace(';','')


def read_text_as_grp(path, seperater = "["):
    _text = []
    with io.open(path, 'r', encoding='utf-8') as f:
        for i, group in enumerate(_get_groups(f,seperater), start = 1):
            _text.append(''.join(group))
    return _text


def input_dt_prcr(t:str):
    t = t.replace(';',' ')
    try:
        _t_title,  _t_process = _blk_prcr(t)
        if _t_title in ['CONDUITS', 'PUMPS']:
            _t_process = _t_process.replace('From Node', 'FromNode')
            _t_process = _t_process.replace('To Node','ToNode')
            if _t_title  == 'PUMPS':
                _t_process = _t_process.replace('Pump Curve','PumpCurve')
        elif _t_title in ['SUBCATCHMENTS','POLYGONS']:
            _t_process = _t_process.replace('Rain Gage', 'RainGage')
        _t_pd = pd.read_csv(StringIO(_t_process), delimiter=' ')
        return {_t_title: _t_pd}
    except:
        pass