=============================================
OpenSRP XLSForm to native form JSON converter
=============================================

|black|

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/python/black

xlson - Converts an OpenSRP data dictionary XLSForm into native form JSON.

----------------------
Installation and Usage
----------------------

Installation
############

`xlson` can be installed by running `python setup.py install`. It requires Python 3.6.0+.

Usage
-----

`xlson` takes an XLSForm e.g `sample.xlsx` as input and outputs a native JSON formatted string to stdout. An example::

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

From the sample XLSForm below::

   | survey   |
   |          | type        | name       | label                   |
   |          | begin group | step1      | Patient Information     |
   |          | text        | first_name | What's your first name? |
   |          | end group   |            |                         |

Contributing to *xlson*.
########################

See `CONTRIBUTING.rst`_ for details.