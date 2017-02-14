{% extends 'docs/source/conf.py.jj2' %}

{%block additional_imports%}
import os
import sys
sys.path.append(os.path.abspath('.'))
{%endblock%}

{%block SPHINX_EXTENSIONS%}
    'pyexcel_sphinx_integration'
{%endblock%}