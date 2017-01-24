Line
--------------------------------------------------------------------------------

.. image:: _static/pline.svg
   :width: 600px
   :height: 400px
		   
Here is the source code using pyexcel::

    >>> import pyexcel as p
    >>> title = 'Browser usage evolution (in %)'
    >>> p.save_as(file_name='line.csv', dest_chart_type='line',
    ...     dest_file_name='pline.svg', dest_title=title)
