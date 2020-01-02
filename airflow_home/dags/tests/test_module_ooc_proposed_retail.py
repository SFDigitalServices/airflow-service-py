""" Tests for ooc_proposed_retail module """
from modules.ooc_proposed_retail import OOCProposedRetail

def test_get_referred_departments():
    """ Test get_referred_departments method """
    proposed_retail = OOCProposedRetail()
    labels = list(proposed_retail.referred_label_map.keys())
    labels.append('Miscellaneous label')

    expected = list(proposed_retail.referred_label_map.values())
    assert proposed_retail.get_referred_departments(labels) == expected
