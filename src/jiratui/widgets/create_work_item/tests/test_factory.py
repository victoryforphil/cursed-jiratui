"""Tests for create work item factory functionality."""

import pytest

from jiratui.widgets.create_work_item.factory import (
    CreateWorkItemFieldId,
    PROCESS_OPTIONAL_FIELDS,
    create_widgets_for_work_item_creation,
)
from jiratui.widgets.create_work_item.fields import CreateWorkItemSelectionInput


def test_sprint_field_id_in_enum():
    """Test that SPRINT is defined in CreateWorkItemFieldId enum."""
    assert CreateWorkItemFieldId.SPRINT.value == 'sprint'


def test_sprint_in_process_optional_fields():
    """Test that sprint is included in PROCESS_OPTIONAL_FIELDS list."""
    assert CreateWorkItemFieldId.SPRINT.value in PROCESS_OPTIONAL_FIELDS


def test_create_widgets_with_sprint_field_with_allowed_values():
    """Test that sprint field creates a selection widget when allowedValues are present."""
    # GIVEN - create metadata with sprint field that has allowedValues
    metadata = [
        {
            'fieldId': 'sprint',
            'name': 'Sprint',
            'required': False,
            'allowedValues': [
                {'id': '1', 'name': 'Sprint 1'},
                {'id': '2', 'name': 'Sprint 2'},
            ],
        }
    ]

    # WHEN
    widgets = create_widgets_for_work_item_creation(metadata)

    # THEN
    assert len(widgets) == 1
    assert isinstance(widgets[0], CreateWorkItemSelectionInput)
    assert widgets[0].id == 'sprint'
    assert widgets[0].border_title == 'Sprint'


def test_create_widgets_with_sprint_field_without_allowed_values():
    """Test that sprint field creates a text widget when allowedValues are not present."""
    # GIVEN - create metadata with sprint field without allowedValues
    metadata = [
        {
            'fieldId': 'sprint',
            'name': 'Sprint',
            'required': False,
        }
    ]

    # WHEN
    widgets = create_widgets_for_work_item_creation(metadata)

    # THEN
    assert len(widgets) == 1
    # Without allowedValues, it falls back to a text field
    assert widgets[0].id == 'sprint'


def test_create_widgets_without_sprint_field():
    """Test that no sprint widget is created when sprint is not in metadata."""
    # GIVEN - create metadata without sprint field
    metadata = [
        {
            'fieldId': 'priority',
            'name': 'Priority',
            'required': False,
            'allowedValues': [
                {'id': '1', 'name': 'High'},
                {'id': '2', 'name': 'Low'},
            ],
        }
    ]

    # WHEN
    widgets = create_widgets_for_work_item_creation(metadata)

    # THEN
    assert len(widgets) == 1
    assert widgets[0].id == 'priority'
    # No sprint widget should be created


def test_create_widgets_sprint_with_multiple_fields():
    """Test that sprint widget is created along with other optional fields."""
    # GIVEN - create metadata with multiple optional fields including sprint
    metadata = [
        {
            'fieldId': 'priority',
            'name': 'Priority',
            'required': False,
            'allowedValues': [
                {'id': '1', 'name': 'High'},
                {'id': '2', 'name': 'Low'},
            ],
        },
        {
            'fieldId': 'sprint',
            'name': 'Sprint',
            'required': False,
            'allowedValues': [
                {'id': '10', 'name': 'Sprint 10'},
                {'id': '11', 'name': 'Sprint 11'},
            ],
        },
        {
            'fieldId': 'duedate',
            'name': 'Due Date',
            'required': False,
        },
    ]

    # WHEN
    widgets = create_widgets_for_work_item_creation(metadata)

    # THEN
    assert len(widgets) == 3
    widget_ids = [w.id for w in widgets]
    assert 'priority' in widget_ids
    assert 'sprint' in widget_ids
    assert 'duedate' in widget_ids


def test_create_widgets_sprint_skipped_fields():
    """Test that sprint is not included in SKIP_FIELDS."""
    # GIVEN - create metadata with sprint and skipped fields
    metadata = [
        {
            'fieldId': 'project',
            'name': 'Project',
            'required': True,
        },
        {
            'fieldId': 'sprint',
            'name': 'Sprint',
            'required': False,
            'allowedValues': [
                {'id': '1', 'name': 'Sprint 1'},
            ],
        },
    ]

    # WHEN
    widgets = create_widgets_for_work_item_creation(metadata)

    # THEN
    # Only sprint widget should be created, project should be skipped
    assert len(widgets) == 1
    assert widgets[0].id == 'sprint'
