# -*- coding: utf-8 -*-
"""
xlson - converts XLSForm to form JSON.
"""
__version__ = "0.0.1"

import json
from enum import Enum
from typing import Any, BinaryIO, Dict

import click
from pyxform.builder import create_survey_element_from_dict
from pyxform.xls2json import parse_file_to_json

CHILDREN = "children"
FIELDS = "fields"
HINT = "hint"
KEY = "key"
LABEL = "label"
NAME = "name"
TITLE = "title"
TYPE = "type"
SUPPORTED_QUESTIONS_TYPES = ["text", "group"]

BIND_CONVERSTION = {"yes": "true", "Yes": "true", "no": "false", "No": "false"}


class QuestionTypes(Enum):
    """XLSForm question types."""

    BARCODE = "barcode"
    GEOPOINT = "geopoint"
    GROUP = "group"
    INTEGER = "integer"
    PHOTO = "photo"
    SELECT_ONE = "select one"
    TEXT = "text"


class NativeFormField(dict):
    """Base class for a native form field."""

    field_type: str = ""

    FIELDS = {
        KEY: str,
        TYPE: str,
        "openmrs_entity": str,
        "openmrs_entity_id": str,
        "openmrs_entity_parent": str,
    }

    def __init__(self, **kwargs: Dict) -> None:
        assert NAME in kwargs, "'%s' is a required field." % KEY
        elements: Dict[str, Any] = {}
        for key, default in self.FIELDS.items():
            elements[key] = kwargs.get(key, default())

        elements[KEY] = kwargs[NAME]
        elements[TYPE] = self.field_type

        if "bind" in kwargs:
            bind_dict: Dict[str, Any] = kwargs.get("bind", {})

            for key, value in bind_dict.items():
                # Handle bind::required value conversion
                if value in BIND_CONVERSTION:
                    val = BIND_CONVERSTION[value]
                    elements["v_required"] = {
                        "value": val,
                        "err": bind_dict.get("jr:requiredMsg"),
                    }

        super(NativeFormField, self).__init__(**elements)


class EditTextField(NativeFormField):
    """Native form edit text field."""

    field_type: str = "edit_text"

    FIELDS = NativeFormField.FIELDS.copy()
    FIELDS.update({"edit_type": str, "hint": str})

    def __init__(self, **kwargs: Dict) -> None:
        assert LABEL in kwargs, "'%s' is a required field." % LABEL
        params: Dict[str, Any] = kwargs.copy()
        params[HINT] = params.pop(LABEL)
        params["edit_type"] = "name"
        super(EditTextField, self).__init__(**params)


class ChooseImageField(NativeFormField):
    """Native form choose_image field."""

    field_type: str = "choose_image"

    FIELDS = NativeFormField.FIELDS.copy()
    FIELDS.update({"uploadButtonText": str})

    def __init__(self, **kwargs: Dict) -> None:
        assert LABEL in kwargs, "'%s' is a required field." % LABEL
        params = kwargs.copy()
        params["uploadButtonText"] = params.pop(LABEL)

        super(ChooseImageField, self).__init__(**params)


class IntegerField(NativeFormField):
    """Native form integer field."""

    field_type: str = "edit_text"

    FIELDS = NativeFormField.FIELDS.copy()
    FIELDS.update({"edit_type": str, "hint": str})

    def __init__(self, **kwargs: Dict) -> None:
        assert LABEL in kwargs, "'%s' is a required field." % LABEL
        params: Dict[str, Any] = kwargs.copy()
        params[HINT] = params.pop(LABEL)
        params["edit_type"] = "number"

        super(IntegerField, self).__init__(**params)


class GpsField(NativeFormField):
    """Native form gps field."""

    field_type: str = "gps"

    FIELDS = NativeFormField.FIELDS.copy()
    FIELDS.update({"openmrs_data_type": str})

    def __init__(self, **kwargs: Dict) -> None:
        assert LABEL in kwargs, "'%s' is a required field." % LABEL
        params: Dict[str, Any] = kwargs.copy()
        # Include the openmrs_data_type field
        params["openmrs_data_type"] = "text"

        super(GpsField, self).__init__(**params)


class BarcodeField(NativeFormField):
    """Native form barcode field."""

    field_type: str = "barcode"

    FIELDS = NativeFormField.FIELDS.copy()
    FIELDS.update({"scanButtonText": str, "barcode_type": str, "hint": str})

    def __init__(self, **kwargs: Dict) -> None:
        assert LABEL in kwargs, "'%s' is a required field." % LABEL
        params: Dict[str, Any] = kwargs.copy()
        params["scanButtonText"] = params.get(HINT)
        params["barcode_type"] = "qrcode"
        params[HINT] = params.pop(LABEL)

        super(BarcodeField, self).__init__(**params)


class NativeRadioField(NativeFormField):
    """Native form native radio field."""

    field_type: str = "native_radio"

    FIELDS = NativeFormField.FIELDS.copy()
    FIELDS.update({"label": str, "options": str})

    def __init__(self, **kwargs: Dict) -> None:
        assert LABEL in kwargs, "'%s' is a required field." % LABEL
        assert CHILDREN in kwargs, "'%s' is a required field." % CHILDREN
        params: Dict[str, Any] = kwargs.copy()

        if CHILDREN in params:
            params["options"] = []
            for child in params[CHILDREN]:
                options_data = {
                    "key": child["name"],
                    "openmrs_entity": "",
                    "openmrs_entity_id": child["instance"]["openmrs_entity_id"],
                    "openmrs_entity_parent": "",
                    "text": child["label"],
                }
                params["options"].append(options_data)
            params.pop("children")

        super(NativeRadioField, self).__init__(**params)


class Step(dict):
    """Native form step section."""

    def __init__(self, **kwargs: Dict) -> None:
        assert LABEL in kwargs, "'%s' is a required field." % LABEL
        assert CHILDREN in kwargs, "'%s' is a required field." % CHILDREN

        elements: Dict[str, Any] = {"title": kwargs[LABEL]}
        elements[FIELDS] = [
            build_field(child)
            for child in kwargs[CHILDREN]
            if child.get(TYPE) in SUPPORTED_QUESTIONS_TYPES
        ]

        super(Step, self).__init__(**elements)


def build_field(options: Dict) -> Dict:
    """Build native field."""
    field: Dict = {}
    if options[TYPE] == QuestionTypes.TEXT.value:
        field = EditTextField(**options)
    elif options[TYPE] == QuestionTypes.GROUP.value:
        field = {options[NAME]: Step(**options)}
    elif options[TYPE] == QuestionTypes.PHOTO.value:
        field = ChooseImageField(**options)
    elif options[TYPE] == QuestionTypes.INTEGER.value:
        field = IntegerField(**options)
    elif options[TYPE] == QuestionTypes.GEOPOINT.value:
        field = GpsField(**options)
    elif options[TYPE] == QuestionTypes.BARCODE.value:
        field = BarcodeField(**options)
    elif options[TYPE] == QuestionTypes.SELECT_ONE.value:
        field = NativeRadioField(**options)

    return field


def create_native_form(survey: Dict) -> Dict:
    """Creates a native form dict."""
    assert NAME in survey
    assert TITLE in survey
    assert TYPE in survey
    assert CHILDREN in survey
    assert len(survey[CHILDREN]) > 1 and survey[CHILDREN][0]

    data = {"encounter_type": survey[TITLE]}
    for child in survey[CHILDREN]:
        is_a_group = child.get(TYPE) == QuestionTypes.GROUP.value
        if is_a_group and child.get(NAME) != "meta":
            data.update(build_field(child))

    return data


@click.command()
@click.argument("xlsform", type=click.File(mode="rb"))
def cli(xlsform: BinaryIO) -> None:
    """xlson - XLSForm to native form JSON."""
    survey = create_survey_element_from_dict(
        parse_file_to_json(xlsform.name, file_object=xlsform)
    )
    form = create_native_form(survey.to_json_dict())
    click.echo(json.dumps(form, indent=4))
