"""
CLI interface for spacexexplorer project.
"""
import tempfile

from spacexexplorer.info_manager import InfoManager
from spacexexplorer.main_manager import MainManager
from spacexexplorer.textui_manager import TextUIManager


def main():  # pragma: no cover
    """
    The main function executes on commands:
    `python -m spacexexplorer` and `$ spacexexplorer `.

    This is spacexexplorer entry point.
    """

    with tempfile.TemporaryDirectory() as tmpdirname:
        info_manager = InfoManager(location=tmpdirname)
        info_manager.fetch_static()
        ui_manager = TextUIManager()
        main = MainManager(info_manager, ui_manager)
        main.main_loop()
