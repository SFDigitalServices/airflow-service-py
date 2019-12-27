""" Test Hello script """
from scripts.hello import says_hello

def test_hello():
    """Test hello"""
    assert says_hello() == "hello"
