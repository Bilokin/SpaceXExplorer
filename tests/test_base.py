import os


def test_base():
    assert os.path.abspath(os.curdir)
