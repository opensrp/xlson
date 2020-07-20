=============================================
OpenSRP XLSForm to native form JSON converter
=============================================

|black| |circleci| |codecov|

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/python/black

.. |circleci| image:: https://circleci.com/gh/OpenSRP/xlson.svg?style=svg
    :target: https://circleci.com/gh/OpenSRP/xlson

.. |codecov| image:: https://codecov.io/github/OpenSRP/xlson/branch/master/graph/badge.svg
    :target: https://codecov.io/github/OpenSRP/xlson

.. _CONTRIBUTING.rst: https://github.com/OpenSRP/xlson/blob/master/CONTRIBUTING.rst

.. _specifications.rst: https://github.com/OpenSRP/xlson/blob/master/docs/specifications.rst

xlson - Converts an OpenSRP data dictionary XLSForm into native form JSON.

--------------
Get the code
--------------

``git clone git@github.com:OpenSRP/xlson.git``

----------------------
Installation and Usage
----------------------

Installation
############

``xlson`` can be installed by running ``python setup.py install``. It requires Python 3.6.0+.
Consider using a `virtualenv <http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/>`_ and `virtualenvwrapper <https://virtualenvwrapper.readthedocs.io/en/latest/>`_
to make dependency management easier

    pip install virtualenv
    pip install virtualenvwrapper
    mkvirtualenv xlson_local                     # or whatever you want to name it
    (xlson_local)$ python setup.py install       # install the required packages required

Usage
-----

``xlson`` takes an XLSForm e.g ``sample.xlsx`` as input and outputs a native JSON formatted string to stdout. An example::

   xlson sample.xlsx > sample.json
   {
       "encounter_type": "sample",
       "step1": {
           "title": "Patient Information",
           "fields": [
               {
                   "key": "first_name",
                   "type": "edit_text",
                   "openmrs_entity": "",
                   "openmrs_entity_id": "",
                   "openmrs_entity_parent": "",
                   "edit_type": "name",
                   "hint": "What's your first name?"
               }
           ]
       }
   }

From the sample XLSForm below:

+-------------+------------+--------------------------+
| type        | name       | label                    |
+=============+============+==========================+
| begin group | step1      | Patient Information      |
+-------------+------------+--------------------------+
| text        | first_name | What's your first name?  |
+-------------+------------+--------------------------+
| end group   |            |                          |
+-------------+------------+--------------------------+

See more on ``xlson`` specifications.rst_.

Contributing to ``xlson``.
##########################

See CONTRIBUTING.rst_ for details.
