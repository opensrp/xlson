# -*- coding: utf-8 -*-
"""
Test xlson python package.
"""

import json
import os
import unittest

from click.testing import CliRunner
from pyxform.tests_v1.pyxform_test_case import PyxformMarkdown

import xlson

HERE = os.path.dirname(__file__)


class TestXLSon(PyxformMarkdown, unittest.TestCase):
    """
    Test xlson package class.
    """

    def setUp(self) -> None:
        self.maxDiff = None  # pylint: disable=invalid-name

    def test_create_native_form(self) -> None:
        """Test xlson.create_native_form() - returns a native form dict structure."""
        sample_md = """
            | survey |
            |        | type        | name       | label               |
            |        | begin group | step1      | Patient Information |
            |        | text        | first_name | What's your name?   |
            |        | end group   |            |                     |
            """
        name = "sample"
        kwargs = {"id_string": name, "name": name, "title": "Sample"}
        survey = self.md_to_pyxform_survey(sample_md, kwargs, False)

        self.assertDictEqual(
            xlson.create_native_form(survey.to_json_dict()),
            {
                "encounter_type": "Sample",
                "step1": {
                    "title": "Patient Information",
                    "fields": [
                        {
                            "edit_type": "name",
                            "hint": "What's your name?",
                            "key": "first_name",
                            "openmrs_entity": "",
                            "openmrs_entity_id": "",
                            "openmrs_entity_parent": "",
                            "type": "edit_text",
                        }
                    ],
                },
            },
        )

    def test_edit_text_field(self) -> None:
        """Test xlson.build_field() - returns a native form field dict."""
        options = {"name": "first_name", "label": "What's your name?", "type": "text"}
        self.assertDictEqual(
            xlson.build_field(options),
            {
                "edit_type": "name",
                "hint": options["label"],
                "key": options["name"],
                "openmrs_entity": "",
                "openmrs_entity_id": "",
                "openmrs_entity_parent": "",
                "type": "edit_text",
            },
        )

    def test_group_field(self) -> None:
        """Test a native form step structure."""
        step = {
            "name": "step1",
            "label": "Patient Information",
            "type": "group",
            "children": [
                {"name": "first_name", "label": "What's your name?", "type": "text"}
            ],
        }
        self.assertDictEqual(
            xlson.build_field(step),
            {
                "step1": {
                    "title": "Patient Information",
                    "fields": [
                        {
                            "edit_type": "name",
                            "hint": "What's your name?",
                            "key": "first_name",
                            "openmrs_entity": "",
                            "openmrs_entity_id": "",
                            "openmrs_entity_parent": "",
                            "type": "edit_text",
                        }
                    ],
                }
            },
        )

    def test_choose_image_field(self) -> None:
        """Test xlson.build_field() - returns a native form choose_image field dict."""
        options = {
            "name": "user_image",
            "label": "Take a photo of the child.",
            "type": "photo",
        }
        self.assertDictEqual(
            xlson.build_field(options),
            {
                "uploadButtonText": options["label"],
                "key": options["name"],
                "openmrs_entity": "",
                "openmrs_entity_id": "",
                "openmrs_entity_parent": "",
                "type": "choose_image",
            },
        )

    def test_number_field(self) -> None:
        """Test xlson.build_field() - returns a native form integer field dict."""
        options = {"name": "user_age", "label": "User age", "type": "integer"}
        self.assertDictEqual(
            xlson.build_field(options),
            {
                "key": "user_age",
                "openmrs_entity_parent": "",
                "openmrs_entity": "",
                "openmrs_entity_id": "",
                "type": "edit_text",
                "hint": "User age",
                "edit_type": "number",
            },
        )

    def test_gps_field(self) -> None:
        """Test xlson.build_field() - returns a native form gps field dict."""
        options = {"name": "user_gps", "label": "GPS", "type": "geopoint"}
        self.assertDictEqual(
            xlson.build_field(options),
            {
                "key": "user_gps",
                "openmrs_entity": "",
                "openmrs_entity_id": "",
                "openmrs_entity_parent": "",
                "openmrs_data_type": "text",
                "type": "gps",
            },
        )

    def test_barcode_field(self) -> None:
        """Test xlson.build_field() - returns a native form barcode field dict"""
        options = {
            "name": "user_qrcode",
            "label": "User ID",
            "hint": "Scan QR code",
            "type": "barcode",
        }
        self.assertDictEqual(
            xlson.build_field(options),
            {
                "key": "user_qrcode",
                "openmrs_entity_parent": "",
                "openmrs_entity": "",
                "openmrs_entity_id": "",
                "type": "barcode",
                "barcode_type": "qrcode",
                "hint": "User ID",
                "scanButtonText": "Scan QR code",
            },
        )

    def test_native_radio_field(self) -> None:
        """Test xlson.build_field() - returns a native form native radio field dict"""
        options = {
            "name": "user_select",
            "label": "Is the child happy?",
            "type": "select one",
            "children": [
                {
                    "name": "yes",
                    "label": "Yes",
                    "instance": {"openmrs_entity_id": "AABB"},
                },
                {
                    "name": "no",
                    "label": "No",
                    "instance": {"openmrs_entity_id": "BBCC"},
                },
            ],
        }  # noqa
        self.assertDictEqual(
            xlson.build_field(options),
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
                        "text": "Yes",
                    },
                    {
                        "key": "no",
                        "openmrs_entity_parent": "",
                        "openmrs_entity": "",
                        "openmrs_entity_id": "BBCC",
                        "text": "No",
                    },
                ],
            },  # noqa
        )

    def test_required_field(self) -> None:
        """Test xlson.build_field() - returns a native form required field dict."""
        options = {
            "name": "first_name",
            "label": "What's your name?",
            "type": "text",
            "bind": {
                "required": "yes",
                "jr:requiredMsg": "Please enter the first name.",
            },
        }
        self.assertDictEqual(
            xlson.build_field(options),
            {
                "key": "first_name",
                "openmrs_entity_parent": "",
                "openmrs_entity": "",
                "openmrs_entity_id": "",
                "type": "edit_text",
                "hint": "What's your name?",
                "edit_type": "name",
                "v_required": {"value": "true", "err": "Please enter the first name."},
            },
        )

    def test_checkbox_field(self) -> None:
        """Test xlson.build_field() - returns a native form checkbox field dict."""
        # Without openmrs_entity_id
        options = {
            "name": "colours",
            "label": "Choose colours you like?",
            "type": "select all that apply",
            "children": [
                {
                    "name": "ze_gree",
                    "label": "Green",
                    "instance": {"openmrs_entity_id": "AABBGRR"},
                },
                {
                    "name": "ze_yellow",
                    "label": "Yellow",
                    "instance": {"openmrs_entity_id": "BBCCYLL"},
                },
            ],
        }
        selected = False
        self.assertDictEqual(
            xlson.build_field(options),
            {
                "key": "colours",
                "openmrs_entity_parent": "",
                "openmrs_entity": "",
                "openmrs_entity_id": "",
                "type": "check_box",
                "label": "Choose colours you like?",
                "options": [
                    {
                        "key": "ze_gree",
                        "text": "Green",
                        "openmrs_choice_id": "AABBGRR",
                        "value": selected
                    },
                    {
                        "key": "ze_yellow",
                        "text": "Yellow",
                        "openmrs_choice_id": "BBCCYLL",
                        "value": selected
                    }
                ]
            },  # noqa
        )

    def test_constraint_field_with_regex_value(self) -> None:
        """Test xlson.build_field() - returns a native form constraint field dict."""
        options = {
            "name": "user_first_name",
            "label": "User First name",
            "type": "text",
            "bind": {
                "jr:constraintMsg": "Please enter a valid name.",
                "constraint": "regex(., '[A-Za-z\\s\\.\\-]*')",
            },
        }
        self.assertDictEqual(
            xlson.build_field(options),
            {
                "key": "user_first_name",
                "openmrs_entity_parent": "",
                "openmrs_entity": "",
                "openmrs_entity_id": "",
                "type": "edit_text",
                "hint": "User First name",
                "edit_type": "name",
                "v_regex": {
                    "value": "[A-Za-z\\s\\.\\-]*",
                    "err": "Please enter a valid name.",
                },
            },
        )

    def test_cli(self) -> None:
        """Test xlson.cli command"""
        runner = CliRunner()
        result = runner.invoke(xlson.cli)
        self.assertIn('Error: Missing argument "XLSFORM".', result.output)
        result = runner.invoke(xlson.cli, args=(os.path.join(HERE, "sample.xlsx"),))

        sample_native_form = {
            "encounter_type": "sample",
            "step1": {
                "title": "Patient Information",
                "fields": [
                    {
                        "edit_type": "name",
                        "hint": "What's your first name?",
                        "key": "first_name",
                        "openmrs_entity": "",
                        "openmrs_entity_id": "",
                        "openmrs_entity_parent": "",
                        "type": "edit_text",
                    }
                ],
            },
        }
        self.assertEqual(sample_native_form, json.loads(result.output))


if __name__ == "__main__":
    unittest.main(module="test_xlson")
