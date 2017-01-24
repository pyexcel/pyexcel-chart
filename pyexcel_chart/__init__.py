"""
    pyexcel_chart
    ~~~~~~~~~~~~~~~~~~~

    chart drawing plugin for pyexcel

    :copyright: (c) 2016-2017 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for further details
"""
import sys
import pygal
from pyexcel.renderers.factory import Renderer

PY2 = sys.version_info[0] == 2
DEFAULT_TITLE = 'pyexcel chart rendered by pygal'
KEYWORD_CHART_TYPE = 'chart_type'
DEFAULT_CHART_TYPE = 'bar'

CHARTS = {
    'bar': 'Bar',
    'line': 'Line',
    'histogram': 'Histogram',
    'xy': 'XY',
    'pie': 'Pie',
    'radar': 'Radar',
    'box': 'Box',
    'dot': 'Dot',
    'funnel': 'Funnel',
    'solidgauge': 'SolidGauge',
    'gauge': 'Gauge',
    'pyramid': 'Pyramid',
    'treemap': 'Treemap',
    'maps': 'Maps'
}


class Chart(Renderer):

    file_types = ('svg',)

    def __init__(self, file_type):
        Renderer.__init__(self, file_type)
        if not PY2:
            self.WRITE_FLAG = 'wb'

    def render_sheet(self, sheet, title=DEFAULT_TITLE,
                     chart_type=DEFAULT_CHART_TYPE, label_x_in_column=0,
                     label_y_in_row=0,
                     **keywords):
        params = {}
        if len(sheet.rownames) == 0:
            sheet.name_rows_by_column(label_x_in_column)
            params['x_labels'] = sheet.rownames
        if len(sheet.colnames) == 0:
            sheet.name_columns_by_row(label_y_in_row)
        the_dict = sheet.to_dict()
        cls_name = CHARTS.get(chart_type)
        cls = getattr(pygal, cls_name)
        instance = cls(title=title, **keywords)
        for key in the_dict:
            data_array = [value for value in the_dict[key] if value != '']
            instance.add(key, data_array)
        chart_content = instance.render()
        if PY2:
            chart_content.decode('utf-8')
        self._stream.write(chart_content)
