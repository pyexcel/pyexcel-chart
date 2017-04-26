"""
    pyexcel_chart
    ~~~~~~~~~~~~~~~~~~~

    chart drawing plugin for pyexcel

    :copyright: (c) 2016-2017 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for further details
"""
from pyexcel.internal.common import PyexcelPluginList


PyexcelPluginList(__name__).add_a_renderer(
    submodule='chart.ChartRenderer',
    file_types=['svg'],
    stream_type='binary'
)
