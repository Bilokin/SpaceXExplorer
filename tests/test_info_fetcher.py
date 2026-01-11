from spacexexplorer.info_manager import InfoManager
import os
import json


def test_launches_as_last_item():
    info = InfoManager()
    key = None
    for key in info.static_file_dict:
        print(key)
    assert key == "launches"


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

def test_rocket_stats():
    info_manager = InfoManager()
    def get_launches():
        launches_objs = [{"success": True, "rocket": 1, "launchpad": 1},
                        {"success": True, "rocket": 1, "launchpad": 1},
                        {"success": False, "rocket": 1, "launchpad": 1},
                        {"success": False, "rocket": 2, "launchpad": 1},
                        {"success": False, "rocket": 2, "launchpad": 1},
                        {"success": True, "rocket": 1, "launchpad": 1},
                        {"success": True, "rocket": 2, "launchpad": 1},
                        {"success": True, "rocket": 2, "launchpad": 1},
        ]
        return launches_objs
    def get_rockets():
        return [{"id": 1}, {"id": 2}]
    def get_lps():
        return [{"id": 1}, {"id": 2}]
    info_manager.static_file_dict = {"rockets": get_rockets,
                                     "launchpads": get_lps,
                                     "launches": get_launches}
    info_manager.fetch_static()
    print(info_manager.static_file_dict)
    assert len(info_manager.rocket_info) > 0
    assert info_manager.rocket_info[1]["successful_launches"] == 3
    assert info_manager.rocket_info[1]["total_launches"] == 4
    assert info_manager.rocket_info[2]["successful_launches"] == 2
    assert info_manager.rocket_info[2]["total_launches"] == 4