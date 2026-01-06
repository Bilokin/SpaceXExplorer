from spacexexplorer.info_manager import InfoManager
import os

def test_fetch_static():
    info = InfoManager()
    info.fetch_static()
    files = os.listdir('.')
    print(files)
    assert len(files) == 4

def test_get():
    info = InfoManager()
    info.fetch_static()
    files = os.listdir('.')
    print(files)
    company = info.get('company')
    assert company is not None
    assert 'headquarters' in company
    assert 'links' in company