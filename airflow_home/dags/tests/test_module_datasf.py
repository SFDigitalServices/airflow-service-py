""" Tests for datasf module """
import os
from unittest.mock import patch
from modules.datasf import DataSF

def test_replace_missing_env():
    """ Test replace method with missing env variable """
    datasf = DataSF()
    assert not datasf.replace('unknown_dataset', {})

def test_replace_exception():
    """ Test replace method with exception """
    datasf = DataSF()
    with patch.dict(os.environ, {'DATASF_ID_UNKNOWN_DATASET':'abc'}):
        with patch('sodapy.Socrata.replace') as mock:
            mock.side_effect = ValueError('ERROR_TEST')
            mock.return_value = True
            resp = datasf.replace('unknown_dataset', {})
            assert not resp
