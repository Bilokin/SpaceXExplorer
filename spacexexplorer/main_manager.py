from spacexexplorer.info_manager import InfoManager
from spacexexplorer.textui_operator import TextUIOperator


class MainManager(object):
    """
    Main manager class that controls the execution loop
    """

    def __init__(self, info_manager: InfoManager, ui_manager: TextUIOperator):
        self.info_manager = info_manager
        self.ui_manager = ui_manager
        self.to_exit = False
        self.greeting = 'This is a SpaceX info app'
        self.main_menu = [("About company", self.about_info),
                          ("Browse launches", self.launches_info),
                          ("Browse landpads", self.landpads_info),
                          ("Browse rockets", self.rockets_info)
                          ]
        self.main_choices = [m[0] for m in self.main_menu]

    def about_info(self):
        pass

    def landpads_info(self):
        pass

    def rockets_info(self):
        pass

    def launches_info(self):
        pass

    def main_loop(self) -> None:
        """
        Creates an infinite loop until the user or an
        external condition breaks it.
        """
        self.ui_manager.say(self.greeting)
        while True:
            msg = 'Choose an action by typing number and pressing ENTER:'
            choice = self.ui_manager.ask_user_choice(
                msg, self.main_choices, ask_exit=True)
            if choice is None:
                self.ui_manager.say(f'Input was not valid, please'
                                    ' enter a valid number!')
                continue
            self.main_menu[choice][1]()
