from spacexexplorer.info_manager import InfoManager
import os
import json

def test_fetch_static():
    info = InfoManager()
    info.fetch_static()
    files = os.listdir('.')
    print(files)
    assert len(files) == len(info.static_file_dict)


def test_get():
    info = InfoManager()
    info.fetch_static()
    files = os.listdir('.')
    print(files)
    company = info.get('company')
    assert company is not None
    assert 'headquarters' in company
    assert 'links' in company


def test_filter_launches():
    info_manager = InfoManager()
    test_objs = [{"success": True},
                     {"success": True},
                     {"success": False},
                     {"success": False},
                     {"success": True},
    ]
    with open( f'launches.json', 'w') as f:
        json.dump(test_objs, f, indent='    ')

    objs = info_manager.get("launches")
    print(objs)
    assert len(objs) == 5

    all_objs = info_manager.filter_launches(**{})
    assert len(objs) == len(all_objs)
    success_objs = info_manager.filter_launches(**{"success": True})
    assert len(success_objs) == 3
    fail_objs = info_manager.filter_launches(**{"success": False})
    assert len(fail_objs) == 2
