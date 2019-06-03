# XLSon Specifications

The purpose of this document is to give a more detailed specification of the xlson project and what exactly it will entail. It is also to outline the many questions that still remain unanswered in hopes to ignite further discussion.

## Introduction and Background

For the OpenSRP team, translation of the data dictionary to its json representation is a manual task that is repetitive and time-consuming. This project seeks to implement the same data dictionary as an extended version of XLSForm with OpenSRP elements. This tool would easen the generation of json objects for the respective xlsforms.

This implementaiton appears to be a feasible project since:
1. There is already an existent tool `pyxform` that handles conversion of XLSForm to JSON.
2. XLSForms have defined field types and in almost all cases there is a 1-1 mapping of xlsform types to native forms.
3. Ona has capacity of authoring forms by non engineers
4. It has a simple language that has [documentation](http://xlsform.org/en/)



## Proposed Structure
**The concept**

The data dictionary is an excel document that specifies the basic data that is used(displayed) on the OpenSRP dashboard. This data has a variety of fields e.g name, type and required that are used to define specific information for that particular record.

The current implementation builds off of the sample data dictionary provided [here](https://docs.google.com/spreadsheets/d/1vQrAzB0LLtR6pskj26znV-xwyyBsYqoa5FdXEKyowco/edit#gid=0), whereby we include and remove columns that are specific to our need at the moment. These columns, as mentioned earlier, are defined field types that have in almost all cases a direct mapping with xlsform field types for instance, or the type, label and name fields.

**Implementation plan**

Initially, for justification of the system, we seek to handle conversion of specific repetitive fields that are manually converted for almost all forms. These fields are:

1. Text
2. Integer
3. Geopoint
4. Relevant
5. Constraint
6. Required
7. Select_one
8. Openmrs_entity
9. Openmrs_entity_id
10. Openmrs_entity_parent

This would allow us to more of define a standard by which these forms would be designed and created, for easy conversion. Which would be a great especially since Ona has the capacity of authoring forms by non engineers.


The following table introduces the proposed mapping for the basic elements within the data dictionary to the corresponding native json elements.

|                     | XLSForm       | Native Json            |
| ------------------- |:-------------:| ----------------------:|
| General elements    | Form Title    | encounter_type <br> `name` : key <br> `label`: hint         |
|                     | Group         | Step <br> `name` : step name <br> `label`: step title       |
| Field elements      | Text          | Edit_text <br> `name` : key <br> `label`: hint              |
|                     | Integer       | Number <br> `name` : key <br> `label`: hint                 |
|                     | Select_one    | Native_radio <br> Text `name` : key <br> Text `label`: hint |
|                     | Select_one <br> choice_list | Options <br> `name` : key <br> `label`: hint  |
|                     | Geopoint      | gps                                                         |
|                     | instance::openmrs_entity_id     | openmrs_entity_id                         |
|                     | instance::openmrs_entity        | openmrs_entity                            |
|                     | instance::openmrs_entity_parent | openmrs_entity_parent                     |
|                     | Relevant field                  | relevant column + other column            |
|                     | Constraint field                | Constraint and constraint message         |
|                     | Required field                  | Required field                            |
|                     | Note*                           | Toaster                                   |


In the case of individual fields to lay a more specific ideation of their proposed structure in Native JSON:

#### Text Field

```
| survey      |                   |               |                           |                                    |
|             | type              | name          | label                     |   instance :: openmrs_entity_id    |
|             | begin group       | step1         | Patient Information       |                     |
|             | text              | first_name    | What's your first name?   |                     |
|             | end group         |               |                           |                     |
```

Will be converted to json using the above mapping to be:

```json
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
```

#### Image Field

```
| type               | name           | label                                |
| photo              | user_image     | Take a photo of the child            |
```

Will be converted to json using the above mapping to be:

```json
{
       "key": "user_image",
       "openmrs_entity_parent": "",
       "openmrs_entity": "",
       "openmrs_entity_id": "",
       "type": "choose_image",
       "uploadButtonText": "Take a photo of the child"
    }
```


#### Select one(Native_radio)

Unlike the current implementation for the data dictionary, whereby the choice_list is within the same sheet, the implementation proposed for the xlson project would be to move this list to a separate sheet. This would align with a standard that is already being implemented within standard .xlsx forms.


```
| survey  |                     |                                     |                      |             |
|         | type                | label                               | name                 | Description                            |
|         | select_one list     | Do you want to select anything      | user_select          | You can select every thing you want.   |
| choices |                     |                  |                   |
|         | list                | Yes              |                   |
|         | list                | No               | no                |
```

Will be converted to json using the above mapping to be:

```json
{
       "key": "user_select",
       "openmrs_entity_parent": "",
       "openmrs_entity": "",
       "openmrs_entity_id": "",
       "type": "native_radio",
       "label": "Do you want to select anything",
       "label_text_style": "bold",
       "text_color": "#000000",
       "label_info_text": "You can select every thing you want.",
       "label_info_title": "User selection",
           "options": [
               {
                   "key": "yes",
                   "openmrs_entity_parent": "",
                   "openmrs_entity": "",
                   "openmrs_entity_id": "",
                   "text": "Yes"
               },
               {
                   "key": "no",
                   "openmrs_entity_parent": "",
                   "openmrs_entity": "",
                   "openmrs_entity_id": "",
                   "text": "No"
               }
           ]
       }
```

#### GPS Field

```
| type              | name          | label                  |
|-------------------|---------------|------------------------|
| gps               | user_gps      | GPS	               	  |
```

Will be converted to json using the above mapping to be:

```json
{
  "key": "gps",
  "openmrs_entity_parent": "",
  "openmrs_entity": "",
  "openmrs_entity_id": "",
  "openmrs_data_type": "text",
  "type": "gps"
}
```

#### Integer Field
```
| type               | name           | label                              |
|--------------------|--------------|--------------------------------------|
| Integer            | user_age      | User age                            |
```
Will be converted to json using the above mapping to be:

```
{
       "key": "user_age",
       "openmrs_entity_parent": "",
       "openmrs_entity": "",
       "openmrs_entity_id": "",
       "type": "number",
       "hint": "User age",
       "edit_type": "number"
     }
```

#### Required Field

```
| type            | name         | label                | required  |  required_message             |
| begin group     | step1        | Patient Information  |           |  Please enter the first name. |
| text            | first_name   | What's your name?    |  yes           |                          |
| end group       |              |                      |                |                          |
```

Will be converted to json using the above mapping to be:

```json
{
  "key": "first_name",
  "openmrs_entity_parent": "",
  "openmrs_entity": "",
  "openmrs_entity_id": "",
  "type": "edit_text",
  "hint": "What's your name? ",
  "edit_type": "name",
  "v_required": {
    "value": "true",
    "err": "Please enter the first name."
  }
}
```

#### Constraint Field

```
| type            | name        | label                | constraint      |  constraint_message|
| begin group     | step1       | Patient Information  |              | Please enter a valid name. |
| text            | first_name  | What's your name     | regex(., "[A-Za-z\\s\\.\\-]*") |          |
| end group       |             |                      |              |                            |
```

Will be converted to json using the above mapping to be:

```json
{
  "key": "user_first_name",
  "openmrs_entity_parent": "",
  "openmrs_entity": "",
  "openmrs_entity_id": "",
  "type": "edit_text",
  "hint": "What's your name",
  "edit_type": "name",
  "v_regex": {
    "value": "[A-Za-z\\s\\.\\-]*",
    "err": "Please enter a valid name."
  }
}
```


