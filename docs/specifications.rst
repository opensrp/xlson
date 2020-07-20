====================
XLSON Specifications
====================

The purpose of this document is to give a more detailed specification of the ``xlson`` project.

Introduction and Background
===========================

For the OpenSRP team, translation of the data dictionary to its JSON representation is a
manual task that is repetitive and time-consuming and requires engineers to be involved
in most of it. The data dictionary is a spreadsheet document that is as an extension to
the XLSForm standard with OpenSRP specific terminology and constructs. The data dictionary
is usually shared with the client to validate the flow of questions and validations. This
project seeks to incorporate the OpenSRP specific facets and generate a native JSON file
from the OpenSRP data dictionary or its equivalent representation conforming to XLSForm
specifications.

Why XLSForm extension?
----------------------

1. There is already an existing tool ``pyxform`` that handles conversion of XLSForm to JSON
   and XML.
2. XLSForms have defined field types, and in almost all cases there is a 1-1 mapping of
   XLSForm types to native forms.
3. Non-engineers can author XLSForms easily.
4. It has a simple language that has `documentation <http://xlsform.org/en/>`_

Where XLSForm falls short?
--------------------------

1. It might not be easy to share the XLSForm data dictionary with the client as currently
   is possible where specific functionality uses colour for visual cues.
2. XLSForm tends to have choices in a separate sheet, whereas a data dictionary might have
   multiple forms in different sheets on the same spreadsheet document.
3. There might be concepts where it is difficult to find a correct XLSForm specification
   to match the required native forms specification, for example, toasters?


Proposed Structure
==================

The plan is to use the title of an XLSForm as the ``encounter_type``. The ``name`` column
in XLSForm becomes the native form ``key`` JSON field. The ``label`` column in XLSForm
becomes the ``hint`` or any equivalent field in native form JSON depending on the field.

Step
----

Native forms tend to have a step or two.  A ``group`` definition ``SHOULD`` be a step. An
OpenSRP data dictionary ``SHOULD always`` have the question fields within a ``group`` in
the XLSForm. For example:

+-------------+------------+-------------------------+
| type        | name       | label                   |
+=============+============+=========================+
| begin group | step1      | Patient Information     |
+-------------+------------+-------------------------+
| text        | first_name | What's your first name? |
+-------------+------------+-------------------------+
| end group   |            |                         |
+-------------+------------+-------------------------+

The above XLSForm results in the native form JSON below::

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

Edit Text Field
---------------

The ``edit_text`` field is XLSForm's ``text`` type.

+-------------+------------+-------------------------+
| type        | name       | label                   |
+=============+============+=========================+
| text        | first_name | What's your first name? |
+-------------+------------+-------------------------+

The resulting native form JSON is::

   {
       "key": "first_name",
       "type": "edit_text",
       "openmrs_entity": "",
       "openmrs_entity_id": "",
       "openmrs_entity_parent": "",
       "edit_type": "name",
       "hint": "What's your first name?"
   }


Edit Text field with openmrs_* properties
-----------------------------------------

To apply ``openmrs_entity*`` to any field use ``instance::openmrs_entity*`` columns in XLSForm. For example:

+-------------+------------+-------------------------+-----------------------------+
| type        | name       | label                   | instance::openmrs_entity_id |
+=============+============+=========================+=============================+
| text        | first_name | What's your first name? | FFAEFDA                     |
+-------------+------------+-------------------------+-----------------------------+

The result native JSON is::

   {
       "key": "first_name",
       "type": "edit_text",
       "openmrs_entity": "",
       "openmrs_entity_id": "FFAEFDA",
       "openmrs_entity_parent": "",
       "edit_type": "name",
       "hint": "What's your first name?"
   }

The same applies to the choices for a radio field or spinner field that are in the ``choices`` sheet in an XLSForm document.

Required Field
--------------

You can define a field as required using the XLSForm's ``required`` and ``required_message`` columns. Here is an example with the ``edit_text`` field.

+-------------+------------+-------------------------+----------+------------------------------+
| type        | name       | label                   | required | required_message             |
+=============+============+=========================+==========+==============================+
| text        | first_name | What's your first name? | yes      | Please enter the first name. |
+-------------+------------+-------------------------+----------+------------------------------+

The resulting native form JSON is::

   {
       "key": "first_name",
       "type": "edit_text",
       "openmrs_entity": "",
       "openmrs_entity_id": "",
       "openmrs_entity_parent": "",
       "edit_type": "name",
       "hint": "What's your first name?",
        "v_required": {
           "value": "true",
           "err": "Please enter the first name."
        }
   }

Constraint Field
----------------

You can define a field as having a constraint using the XLSForm's ``constraint`` and ``constraint_message`` columns. Here is an example with the ``edit_text`` field.

+-------------+------------+-------------------------+---------------------------------+----------------------------+
| type        | name       | label                   | constraint                      | constraint_message         |
+=============+============+=========================+=================================+============================+
| text        | first_name | What's your first name? | regex(., "[A-Za-z\\s\\.\\-]*")  | Please enter a valid name. |
+-------------+------------+-------------------------+---------------------------------+----------------------------+

The resulting native form JSON is::

   {
       "key": "first_name",
       "type": "edit_text",
       "openmrs_entity": "",
       "openmrs_entity_id": "",
       "openmrs_entity_parent": "",
       "edit_type": "name",
       "hint": "What's your first name?",
        "v_regex": {
           "value": "[A-Za-z\\s\\.\\-]*",
           "err": "Please enter a valid name."
        }
   }

Number Field
------------

The ``number`` field is XLSForm's ``integer`` type.

+-------------+------------+-------------------------+
| type        | name       | label                   |
+=============+============+=========================+
| text        | age        | Patient's age (years)?  |
+-------------+------------+-------------------------+

The resulting native form JSON is::

   {
       "key": "first_name",
       "type": "edit_text",
       "openmrs_entity": "",
       "openmrs_entity_id": "",
       "openmrs_entity_parent": "",
       "edit_type": "number",
       "hint": "Patient's age (years)?"
   }

GPS Field
---------

The ``gps`` field is XLSForm's ``geopoint`` type.

+-------------+------------+-------------------------+
| type        | name       | label                   |
+=============+============+=========================+
| gps         | user_gps   | Capture GPS             |
+-------------+------------+-------------------------+

The resulting native form JSON is::

   {
       "key": "user_gps",
       "type": "gps",
       "openmrs_entity": "",
       "openmrs_entity_id": "",
       "openmrs_entity_parent": "",
       "openmrs_data_type": "text",
   }

Choose Image Field
------------------

The ``choose_image`` field is XLSForm's ``photo`` type.

+-------------+------------+------------------------------+
| type        | name       | label                        |
+=============+============+==============================+
| photo       | user_image | Take a photo of the patient. |
+-------------+------------+------------------------------+

The resulting native form JSON is::

   {
       "key": "user_image",
       "type": "choose_image",
       "openmrs_entity": "",
       "openmrs_entity_id": "",
       "openmrs_entity_parent": "",
       "uploadButtonText": "Take a photo of the patient.",
   }

Native Radio Field
------------------

The ``native_radio`` field is XLSForm's ``select one`` type.

survey sheet

+--------------------+-------------+------------------------------+
| type               | name        | label                        |
+====================+=============+==============================+
| select one yes_no  | user_select | Is the child happy?          |
+--------------------+-------------+------------------------------+

choices sheet

+--------------------+-------------+---------+-----------------------------+
| list name          | name        | label   | instance::openmrs_entity_id |
+====================+=============+=========+=============================+
| yes_no             | yes         | Yes     | AABB                        |
+--------------------+-------------+---------+-----------------------------+
| yes_no             | no          | No      | BBCC                        |
+--------------------+-------------+---------+-----------------------------+

The resulting native form JSON is::

   {
     "key": "user_select",
     "openmrs_entity_parent": "",
     "openmrs_entity": "",
     "openmrs_entity_id": "",
     "type": "native_radio",
     "label": "Is the child happy?",
     "options": [
       {
         "key": "yes",
         "openmrs_entity_parent": "",
         "openmrs_entity": "",
         "openmrs_entity_id": "AABB",
         "text": "Yes"
       },
       {
         "key": "no",
         "openmrs_entity_parent": "",
         "openmrs_entity": "",
         "openmrs_entity_id": "BBCC",
         "text": "No"
       }
     ]
   }

Spinner Field
-------------

The ``spinner`` field is XLSForm's ``select one`` type.

survey sheet

+------------------------+--------------+--------------------+--------------------+
| type                   | name         | label              | hint               |
+========================+==============+====================+====================+
| select multiple moods  | user_spinner | What is the mood?  | What is the mood?  |
+------------------------+--------------+--------------------+--------------------+

choices sheet

+-------------------+-------------+---------+---------------------------------------+
| list name         | name        | label   | instance::openmrs_entity_id           |
+===================+=============+=========+=======================================+
| moods             | happy       | Happy   | 1107AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA  |
+-------------------+-------------+---------+---------------------------------------+
| moods             | sad         | Sad     | 1713AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA  |
+-------------------+-------------+---------+---------------------------------------+
| moods             | somber      | Somber  | 2113AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA  |
+-------------------+-------------+---------+---------------------------------------+

The resulting native form JSON is::

   {
     "key": "user_spinner",
     "openmrs_entity_parent": "",
     "openmrs_entity": "",
     "openmrs_entity_id": "",
     "type": "spinner",
     "hint": "What is the mood?",
      "options": [
         {
            "key": "happy",
            "openmrs_entity": "",
            "openmrs_entity_id": "1107AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
            "openmrs_entity_parent": "",
            "text": "Happy"
         },
         {
            "key": "sad",
            "openmrs_entity": "",
            "openmrs_entity_id": "1713AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
            "openmrs_entity_parent": "",
            "text": "Sad"
         },
          {
            "key": "somber",
            "openmrs_entity": "",
            "openmrs_entity_id": "2113AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
            "openmrs_entity_parent": "",
            "text": "Somber"
         }
      ]
   }

Barcode Field
-------------

The ``barcode`` field is XLSForm's ``barcode`` type.

+-------------+-------------+---------+--------------------+
| type        | name        | label   | hint               |
+=============+=============+=========+====================+
| barcode     | user_qrcode | User ID | Scan QR Code       |
+-------------+-------------+---------+--------------------+

The resulting native form JSON is::

   {
     "key": "user_qrcode",
     "openmrs_entity_parent": "",
     "openmrs_entity": "",
     "openmrs_entity_id": "",
     "type": "barcode",
     "barcode_type": "qrcode",
     "hint": "User ID",
     "scanButtonText": "Scan QR Code",
   }

Multi-language Support
----------------------

Using XLSForm's multi-language support, it should be possible to generate an equivalent
multi-language native form JSON.

+-------------+------------+-------------------------+-----------------------+
| type        | name       | label::English          | label::German         |
+=============+============+=========================+=======================+
| text        | first_name | What's your first name? | Wie ist dein Vorname? |
+-------------+------------+-------------------------+-----------------------+

The resulting native form JSON is::

   {
       "key": "first_name",
       "type": "edit_text",
       "openmrs_entity": "",
       "openmrs_entity_id": "",
       "openmrs_entity_parent": "",
       "edit_type": "name",
       "hint": "What's your first name?"
   }

