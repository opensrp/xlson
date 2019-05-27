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
        """Test xlson.build_field() - returns a native form field dict"""
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