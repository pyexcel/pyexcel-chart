"""
    pyexcel_chart
    ~~~~~~~~~~~~~~~~~~~

    chart drawing plugin for pyexcel

    :copyright: (c) 2016-2017 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for further details
"""
import sys
import pygal
from functools import partial

from lml.plugin import PluginInfo, PluginManager

from pyexcel.renderer import Renderer


PY2 = sys.version_info[0] == 2
DEFAULT_TITLE = 'pyexcel chart rendered by pygal'
KEYWORD_CHART_TYPE = 'chart_type'
DEFAULT_CHART_TYPE = 'bar'
CHART_TYPES = dict(
    pie='Pie',
    box='Box',
    line='Line',
    bar='Bar',
    stacked_bar='StackedBar',
    radar='Radar',
    dot='Dot',
    funnel='Funnel',
    xy='XY',
    histogram='Histogram')


if PY2:
    from StringIO import StringIO as BytesIO
else:
    from io import BytesIO


class Chart(object):

    def __init__(self, cls_name):
        self._chart_class = CHART_TYPES.get(cls_name, 'line')


@PluginInfo('chart', tags=['pie', 'box'])
class SimpleLayout(Chart):

    def render_sheet(self, sheet, title=DEFAULT_TITLE,
                     label_y_in_row=0,
                     **keywords):
        params = {}
        self.params = {}
        if len(sheet.colnames) == 0:
            sheet.name_columns_by_row(label_y_in_row)
        params.update(keywords)
        the_dict = sheet.to_dict()
        cls = getattr(pygal, self._chart_class)
        instance = cls(title=title, **params)
        for key in the_dict:
            data_array = [value for value in the_dict[key] if value != '']
            instance.add(key, data_array)
        chart_content = instance.render()
        return chart_content


@PluginInfo('chart',
          tags=['line', 'bar', 'stacked_bar', 'radar', 'dot', 'funnel'])
class ComplexLayout(Chart):

    def render_sheet(self, sheet, title=DEFAULT_TITLE,
                     label_x_in_column=0, label_y_in_row=0,
                     **keywords):
        params = {}
        self.params = {}
        if len(sheet.colnames) == 0:
            sheet.name_columns_by_row(label_y_in_row)
        if len(sheet.rownames) == 0:
            sheet.name_rows_by_column(label_x_in_column)
        params['x_labels'] = sheet.rownames
        params.update(keywords)
        the_dict = sheet.to_dict()
        cls = getattr(pygal, self._chart_class)
        instance = cls(title=title, **params)
        for key in the_dict:
            data_array = [value for value in the_dict[key] if value != '']
            instance.add(key, data_array)
        chart_content = instance.render()
        return chart_content


@PluginInfo('chart', tags=['histogram'])
class Histogram(Chart):
    def render_sheet(self, sheet, title=DEFAULT_TITLE,
                     height_in_column=0, start_in_column=1,
                     stop_in_column=2,
                     **keywords):
        histograms = zip(sheet.column[height_in_column],
                         sheet.column[start_in_column],
                         sheet.column[stop_in_column])
        cls = getattr(pygal, self._chart_class)
        instance = cls(title=title, **keywords)
        instance.add(sheet.name, histograms)
        chart_content = instance.render()
        return chart_content

    def render_book(self, book, title=DEFAULT_TITLE,
                    height_in_column=0, start_in_column=1,
                    stop_in_column=2,
                    **keywords):
        from pyexcel.book import to_book
        cls = getattr(pygal, self._chart_class)
        instance = cls(title=title, **keywords)
        for sheet in to_book(book):
            histograms = zip(sheet.column[height_in_column],
                             sheet.column[start_in_column],
                             sheet.column[stop_in_column])
            instance.add(sheet.name, histograms)
        chart_content = instance.render()
        return chart_content


@PluginInfo('chart', tags=['xy'])
class XY(Chart):

    def render_sheet(self, sheet, title=DEFAULT_TITLE,
                     x_in_column=0,
                     y_in_column=1,
                     **keywords):
        cls = getattr(pygal, self._chart_class)
        instance = cls(title=title, **keywords)
        points = zip(sheet.column[x_in_column],
                     sheet.column[y_in_column])
        instance.add(sheet.name, points)
        chart_content = instance.render()
        return chart_content

    def render_book(self, book, title=DEFAULT_TITLE,
                    x_in_column=0,
                    y_in_column=1,
                    **keywords):
        from pyexcel.book import to_book
        cls = getattr(pygal, self._chart_class)
        instance = cls(title=title, **keywords)
        for sheet in to_book(book):
            points = zip(sheet.column[x_in_column],
                         sheet.column[y_in_column])
            instance.add(sheet.name, points)
        chart_content = instance.render()
        return chart_content


class ChartManager(PluginManager):
    def __init__(self):
        PluginManager.__init__(self, 'chart')

    def get_a_plugin(self, key, **keywords):
        self._logger.debug("get a plugin called")
        plugin = self.load_me_now(key)
        return plugin(key)

    def raise_exception(self, key):
        raise Exception("No support for " + key)

MANAGER = ChartManager()

class ChartRenderer(Renderer):

    def __init__(self, file_type):
        Renderer.__init__(self, file_type)
        if not PY2:
            self.WRITE_FLAG = 'wb'

    def get_io(self):
        io = BytesIO()

        def repr_svg(self):
            return self.getvalue().decode('utf-8')

        io._repr_svg_ = partial(repr_svg, io)
        return io

    def render_sheet(self, sheet, title=DEFAULT_TITLE,
                     chart_type=DEFAULT_CHART_TYPE,
                     **keywords):
        charter = MANAGER.get_a_plugin(chart_type)
        chart_content = charter.render_sheet(
            sheet, title=title, **keywords)
        self._write_content(chart_content)

    def render_book(self, book, title=DEFAULT_TITLE,
                    chart_type=DEFAULT_CHART_TYPE, **keywords):
        charter = MANAGER.get_a_plugin(chart_type)
        chart_content = charter.render_book(book,
                                            title=title,
                                            **keywords)
        self._write_content(chart_content)

    def _write_content(self, chart_content):
        if PY2:
            chart_content.decode('utf-8')
        self._stream.write(chart_content)
