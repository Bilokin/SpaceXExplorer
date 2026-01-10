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

        self.launches_menu = [
            ("All", self.info_manager.filter_launches, {}),
            ("Successful", self.info_manager.filter_launches,
             {"success": True}),
            ("Failed", self.info_manager.filter_launches,
             {"success": False})
        ]
        self.launch_choices = [m[0] for m in self.launches_menu]

    def about_info(self) -> None:
        """
        Prints info about the company
        """
        info = self.info_manager.get("company")
        properties = ['name', 'founded', 'summary',
                      'employees',  'vehicles', 'ceo']
        self.ui_manager.separator()
        for prop in properties:
            self.ui_manager.say(f"{prop.capitalize()}: {info.get(prop)}")
        self.ui_manager.separator()

    def landpads_info(self) -> None:
        pass

    def rockets_info(self) -> None:
        pass

    def show_launch_info(self, launch: dict) -> None:
        properties = ['date_local', 'flight_number',
                      'name', 'success', 'reused',
                      'landing_success',  'details']
        self.ui_manager.separator()
        self.ui_manager.say("Launch information")
        self.ui_manager.separator()
        for prop in properties:
            self.ui_manager.say(
                f"{prop.capitalize().replace('_', ' ')}: {launch.get(prop)}")
        self.ui_manager.separator()

    def launches_info(self) -> None:
        msg = 'Choose an action by typing number and pressing ENTER:'
        while True:
            choice = self.ui_manager.ask_user_choice(
                msg, self.launch_choices, ask_exit=True)
            if choice is None:
                self.ui_manager.say('Input was not valid, please'
                                    ' enter a valid number!')
                continue
            filtered = self.launches_menu[choice][1](
                **self.launches_menu[choice][2])
            launch_list_menu = [launch['date_local'].split(
                'T')[0] for launch in filtered]
            msg_launch = 'Choose date by typing number and pressing ENTER:'
            choice_launch = self.ui_manager.ask_user_choice(
                msg_launch, launch_list_menu, ask_exit=True)
            if choice_launch is None:
                self.ui_manager.say('Input was not valid, please'
                                    ' enter a valid number!')
            else:
                self.show_launch_info(filtered[choice_launch])
                break

    def main_loop(self) -> None:
        """
        Creates an infinite loop until the user or an
        external condition breaks it.
        """
        self.ui_manager.say(self.greeting)
        msg = 'Choose an action by typing number and pressing ENTER:'
        while True:
            choice = self.ui_manager.ask_user_choice(
                msg, self.main_choices, ask_exit=True)
            if choice is None:
                self.ui_manager.say('Input was not valid, please'
                                    ' enter a valid number!')
                continue
            self.main_menu[choice][1]()
