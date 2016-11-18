"""
    pyexcel_chart
    ~~~~~~~~~~~~~~~~~~~

    drawing plugin for pyexcel

    :copyright: (c) 2016 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for further details
"""
import pygal
from pyexcel.renderers.factory import Renderer

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

    def render_sheet(self, sheet, title=DEFAULT_TITLE,
                     chart_type=DEFAULT_CHART_TYPE, **keywords):
        if len(sheet.colnames) == 0:
            sheet.name_columns_by_row(0)
        the_dict = sheet.to_dict()
        cls_name = CHARTS.get(chart_type)
        cls = getattr(pygal, cls_name)
        bar = cls(title=title, **keywords)
        for key in the_dict:
            bar.add(key, [value for value in the_dict[key] if value !=''])
        self.stream.write(bar.render())
