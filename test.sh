pip freeze
nosetests --with-cov --cover-package pyexcel_chart --cover-package tests --with-doctest --doctest-extension=.rst README.rst tests docs/source pyexcel_chart && flake8 . --exclude=.moban.d --builtins=unicode,xrange,long

mv -v *.svg docs/source/_static


