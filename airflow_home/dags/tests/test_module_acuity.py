"""Test functions from modules/acuity"""
from modules.acuity import Acuity

SAMPLE_FORM_VALUES = [
    {
        'id': 1110646223,
        'fieldID': 7514073,
        'value': '000000',
        'name': 'DSW Number'
    },
    {
        'id': 1110646228,
        'fieldID': 7543629,
        'value': 'no',
        'name': 'Are you driving to the site?'
    }
]

SAMPLE_APPOINTMENT_WITH_FORMS = {
    'forms': [
        {
            'id': 1368026,
            'name': '',
            'values': [
                {
                    'id': 1110646223,
                    'fieldID': 7514073,
                    'value': '000000',
                    'name': 'DSW Number'
                },
                {
                    'id': 1110646228,
                    'fieldID': 7543629,
                    'value': 'no',
                    'name': 'Are you driving to the site?'
                }
            ]
        },
        {
            'id': 1369277,
            'name': 'Drive-thru testing verification (Internal Use)',
            'values': [
                {
                    'id': 1110646226,
                    'fieldID': 7521384,
                    'value': 'RevoWPSFVZRPXLAFqwdF8iJPokTL4LTx4KebKNMUNMBsyEPgCXk2hvAuwo1HMEX',
                    'name': 'Token'
                },
                {
                    'id': 1110646220,
                    'fieldID': 7570420,
                    'value': '5e9892399e7436203dfe7250',
                    'name': 'External ID'
                }
            ]
        }
    ]
}

def test_get_form_value_present():
    """Verify that get_form_value can access a value if present."""
    value = Acuity.get_form_value(SAMPLE_FORM_VALUES, 7514073)
    assert value == '000000'


def test_get_form_value_empty_form():
    """
    Verify that get_form_value fails gracefully if the form does not exist
    or has no values.
    """
    value = Acuity.get_form_value([], 7514073)
    assert value is None

def test_get_form_value_missing_field():
    """Verify that get_form_value fails gracefully if the id is not found."""
    value = Acuity.get_form_value(SAMPLE_FORM_VALUES, 'wrong_id')
    assert value is None

def test_get_form_values_success():
    """Verify we can parse form values successfully."""
    values = Acuity.get_form_values(SAMPLE_APPOINTMENT_WITH_FORMS, 1368026)
    expected_values = [
        {
            'id': 1110646223,
            'fieldID': 7514073,
            'value': '000000',
            'name': 'DSW Number'
        },
        {
            'id': 1110646228,
            'fieldID': 7543629,
            'value': 'no',
            'name': 'Are you driving to the site?'
        }
    ]

    assert values == expected_values


def test_get_form_values_missing():
    """Verify we can parse form values successfully."""
    values = Acuity.get_form_values(SAMPLE_APPOINTMENT_WITH_FORMS, 'wrong_id')
    assert values == []
