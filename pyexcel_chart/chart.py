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
from pyexcel.renderers import Renderer
from pyexcel._compact import with_metaclass


PY2 = sys.version_info[0] == 2
DEFAULT_TITLE = 'pyexcel chart rendered by pygal'
KEYWORD_CHART_TYPE = 'chart_type'
DEFAULT_CHART_TYPE = 'bar'


if PY2:
    from StringIO import StringIO as BytesIO
else:
    from io import BytesIO


_charts = []


def register_class(cls):
    _charts.append(cls)


class MetaForChartRegistryOnly(type):
    """sole class registry"""
    def __init__(cls, name, bases, nmspc):
        super(MetaForChartRegistryOnly, cls).__init__(
            name, bases, nmspc)
        register_class(cls)


class Chart(with_metaclass(MetaForChartRegistryOnly, object)):
    chart_types = dict()

    def __init__(self, cls_name):
        self._chart_class = self.chart_types.get(cls_name, 'line')


class SimpleLayout(Chart):
    chart_types = dict(
        pie='Pie',
        box='Box'
    )

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


class ComplexLayout(Chart):
    chart_types = dict(
        line='Line',
        bar='Bar',
        stacked_bar='StackedBar',
        radar='Radar',
        dot='Dot',
        funnel='Funnel'
    )

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


class Histogram(Chart):
    chart_types = dict(
        histogram='Histogram'
    )

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


class XY(Chart):
    chart_types = dict(
        xy='XY'
    )

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


def create_chart_factory(chart_type):
    for cls in _charts:
        if chart_type in cls.chart_types.keys():
            instance = cls(chart_type)
            return instance
    else:
        raise Exception("No support for " + chart_type)


class ChartRenderer(Renderer):

    file_types = ('svg',)

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
        charter = create_chart_factory(chart_type)
        chart_content = charter.render_sheet(
            sheet, title=title, **keywords)
        self._write_content(chart_content)

    def render_book(self, book, title=DEFAULT_TITLE,
                    chart_type=DEFAULT_CHART_TYPE, **keywords):
        charter = create_chart_factory(chart_type)
        chart_content = charter.render_book(book,
                                            title=title,
                                            **keywords)
        self._write_content(chart_content)

    def _write_content(self, chart_content):
        if PY2:
            chart_content.decode('utf-8')
        self._stream.write(chart_content)
