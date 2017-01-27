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
from pyexcel.renderers.factory import Renderer


PY2 = sys.version_info[0] == 2
DEFAULT_TITLE = 'pyexcel chart rendered by pygal'
KEYWORD_CHART_TYPE = 'chart_type'
DEFAULT_CHART_TYPE = 'bar'


if PY2:
    from StringIO import StringIO as BytesIO
else:
    from io import BytesIO


class ExPie(object):
    def __init__(self):
        self._chart_class = 'Pie'

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


class ExLine(object):
    def __init__(self):
        self._chart_class = 'Line'

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


class ExRadar(ExLine):
    def __init__(self):
        self._chart_class = 'Radar'


class ExDot(ExLine):
    def __init__(self):
        self._chart_class = 'Dot'


class ExFunnel(ExLine):
    def __init__(self):
        self._chart_class = 'Funnel'


class ExBox(ExPie):
    def __init__(self):
        self._chart_class = 'Box'


class ExHistogram(object):
    def __init__(self):
        self.__chart_class = 'Histogram'

    def render_sheet(self, sheet, title=DEFAULT_TITLE,
                     height_in_column=0, start_in_column=1,
                     stop_in_column=2,
                     **keywords):
        histograms = zip(sheet.column[height_in_column],
                         sheet.column[start_in_column],
                         sheet.column[stop_in_column])
        cls = getattr(pygal, self.__chart_class)
        instance = cls(title=title, **keywords)
        instance.add(sheet.name, histograms)
        chart_content = instance.render()
        return chart_content

    def render_book(self, book, title=DEFAULT_TITLE,
                    height_in_column=0, start_in_column=1,
                    stop_in_column=2,
                    **keywords):
        from pyexcel.book import to_book
        cls = getattr(pygal, self.__chart_class)
        instance = cls(title=title, **keywords)
        for sheet in to_book(book):
            histograms = zip(sheet.column[height_in_column],
                             sheet.column[start_in_column],
                             sheet.column[stop_in_column])
            instance.add(sheet.name, histograms)
        chart_content = instance.render()
        return chart_content


class ExXY(object):
    def __init__(self):
        self.__chart_class = 'XY'

    def render_sheet(self, sheet, title=DEFAULT_TITLE,
                     x_in_column=0,
                     y_in_column=1,
                     **keywords):
        cls = getattr(pygal, self.__chart_class)
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
        cls = getattr(pygal, self.__chart_class)
        instance = cls(title=title, **keywords)
        for sheet in to_book(book):
            points = zip(sheet.column[x_in_column],
                         sheet.column[y_in_column])
            instance.add(sheet.name, points)
        chart_content = instance.render()
        return chart_content


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

    def get_io(self):
        io = BytesIO()
        def repr_svg(self):
            return self.getvalue().decode('utf-8')
        io._repr_svg_ = partial(repr_svg, io)
        return io

    def render_sheet(self, sheet, title=DEFAULT_TITLE,
                     chart_type=DEFAULT_CHART_TYPE, label_x_in_column=0,
                     label_y_in_row=0,
                     **keywords):
        if chart_type == 'line':
            xline = ExLine()
            chart_content = xline.render_sheet(
                sheet, title=title,
                label_x_in_column=label_x_in_column,
                label_y_in_row=label_y_in_row, **keywords)
        elif chart_type == 'line':
            xline = ExDot()
            chart_content = xline.render_sheet(
                sheet, title=title,
                label_x_in_column=label_x_in_column,
                label_y_in_row=label_y_in_row, **keywords)
        elif chart_type == 'line':
            xline = ExFunnel()
            chart_content = xline.render_sheet(
                sheet, title=title,
                label_x_in_column=label_x_in_column,
                label_y_in_row=label_y_in_row, **keywords)
        elif chart_type == 'pie':
            xline = ExPie()
            chart_content = xline.render_sheet(
                sheet, title=title,
                label_y_in_row=label_y_in_row, **keywords)
        elif chart_type == 'histogram':
            xhisto = ExHistogram()
            chart_content = xhisto.render_sheet(
                sheet, title=title
            )
        elif chart_type == 'xy':
            xhisto = ExXY()
            chart_content = xhisto.render_sheet(
                sheet, title=title, **keywords
            )
        elif chart_type == 'radar':
            xhisto = ExRadar()
            chart_content = xhisto.render_sheet(
                sheet, title=title,
                label_x_in_column=label_x_in_column,
                label_y_in_row=label_y_in_row, **keywords)
        elif chart_type == 'box':
            xhisto = ExBox()
            chart_content = xhisto.render_sheet(
                sheet, title=title,
                label_y_in_row=label_y_in_row, **keywords)
        else:
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

    def render_book(self, book, title=DEFAULT_TITLE,
                    chart_type=DEFAULT_CHART_TYPE, **keywords):
        if chart_type == 'histogram':
            xhisto = ExHistogram()
            chart_content = xhisto.render_book(
                book, title=title
            )
        elif chart_type == 'xy':
            xhisto = ExXY()
            chart_content = xhisto.render_book(
                book, title=title
            )
        if PY2:
            chart_content.decode('utf-8')
        self._stream.write(chart_content)
