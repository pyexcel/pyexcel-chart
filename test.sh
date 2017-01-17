

pip freeze
nosetests --with-cov --cover-package pyexcel_chart --cover-package tests --with-doctest --doctest-extension=.rst tests README.rst docs/source pyexcel_chart && flake8 . --exclude=.moban.d --builtins=unicode,xrange,long

mv *.svg docs/source/_static


