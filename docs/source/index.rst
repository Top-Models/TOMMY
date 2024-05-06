Welcome to TOMMY's wiki!
========================

**Tommy** is an application that makes topic modelling easy and accessible, developed for EMMA by students from Utrecht University.

.. image:: _static/tommy.png
    :width: 100

Download
========

- :download:`TOMMY for Mac <download/tommy-mac.dmg>`
- :download:`TOMMY for Windows <download/tommy-windows.zip>`
- :download:`TOMMY for Linux <download/tommy-linux.zip>`

.. toctree::
    :maxdepth: 1
    :caption: User wiki

    wiki-user/User-guide.md

.. toctree::
    :maxdepth: 1
    :caption: Developer wiki

    wiki-dev/Style-guide.md
    wiki-dev/Style-guide-source-control.md
    wiki-dev/Generating-Portable-Executable.md
    wiki-dev/How-to-run-tests-from-PyCharm.md
    wiki-dev/Writing-unit-tests-with-PyTest.md

Code documentation
==================

.. autosummary::
    :toctree: code
    :caption: Code documentation
    :recursive:

    tommy
    tommy.view
    tommy.controller
    tommy.model