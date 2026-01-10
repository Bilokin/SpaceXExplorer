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
        self.greeting = "This is a SpaceX info app"
        self.define_menus()

    def define_menus(self):
        self.main_menu = [("About company", self.about_info),
                          ("Browse launches", self.launches_loop),
                          ("Browse launchpads", self.show_launchpads_menu),
                          ("Browse rockets", self.show_rockets_menu)
                          ]
        self.main_choices = [m[0] for m in self.main_menu]

        self.launches_menu = [
            ("All", self.info_manager.filter_launches, {}),
            ("Successful", self.info_manager.filter_launches,
             {"success": True}),
            ("Failed", self.info_manager.filter_launches,
             {"success": False})
        ]
        for rocket_id in self.info_manager.rocket_info:
            name = self.info_manager.rocket_info[rocket_id]
            item = (f"By {name} rocket",
                    self.info_manager.filter_launches,
                    {"rocket": rocket_id})
            self.launches_menu.append(item)
        for launchpad_id in self.info_manager.launchpad_info:
            name = self.info_manager.launchpad_info[launchpad_id]
            item = (f"By {name}",
                    self.info_manager.filter_launches,
                    {"launchpad": launchpad_id})
            self.launches_menu.append(item)
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

    def show_single_launchpad_info(self, launchpad: dict) -> None:
        self.ui_manager.separator()
        self.ui_manager.say("Launchpad information")
        self.ui_manager.separator()
        properties = ['full_name', 'locality',
                      'region', 'status',
                      'launch_attempts', 'launch_successes',
                      'details'
                      ]
        for prop in properties:
            self.ui_manager.say(
                f"{prop.capitalize().replace('_', ' ')}: {launchpad.get(prop)}")
        self.ui_manager.separator()

    def show_launchpads_menu(self) -> None:
        msg = "\nChoose a launchpad by typing a number and pressing [ENTER]:"
        all_lps = self.info_manager.get("launchpads")
        lps_menu = [self.info_manager.launchpad_info[key]
                    for key in self.info_manager.launchpad_info]
        choice = self.ui_manager.ask_user_choice(
            msg, lps_menu, ask_exit=True)
        if choice is None:
            self.ui_manager.say('Input was not valid, please'
                                ' enter a valid number!')
            return
        for lp in all_lps:
            if lp.get('full_name') == lps_menu[choice]:
                self.show_single_launchpad_info(lp)
                break

    def show_single_rocket_info(self, rocket: dict) -> None:
        self.ui_manager.separator()
        self.ui_manager.say("Rocket information")
        self.ui_manager.separator()
        properties = ['name', 'type',
                      'active', 'stages', 'reusable',
                      'description']
        for prop in properties:
            self.ui_manager.say(
                f"{prop.capitalize().replace('_', ' ')}: {rocket.get(prop)}")
        self.ui_manager.separator()

    def show_rockets_menu(self) -> None:
        msg = '\nChoose a rocket by typing a number and pressing [ENTER]:'
        all_rockets = self.info_manager.get("rockets")
        rockets_menu = [self.info_manager.rocket_info[key]
                        for key in self.info_manager.rocket_info]
        choice = self.ui_manager.ask_user_choice(
            msg, rockets_menu, ask_exit=True)
        if choice is None:
            self.ui_manager.say('Input was not valid, please'
                                ' enter a valid number!')
            return
        for rocket in all_rockets:
            if rocket.get('name') == rockets_menu[choice]:
                self.show_single_rocket_info(rocket)
                break

    def show_single_launch_info(self, launch: dict) -> None:
        properties = ['date_local', 'flight_number',
                      'name', 'success', 'reused',
                      'landing_success',  'details']
        self.ui_manager.separator()
        self.ui_manager.say("Launch information")
        self.ui_manager.separator()
        rocket_name = self.info_manager.rocket_info.get(launch.get('rocket'))
        self.ui_manager.say(f"Rocket: {rocket_name}")
        for prop in properties:
            self.ui_manager.say(
                f"{prop.capitalize().replace('_', ' ')}: {launch.get(prop)}")
        self.ui_manager.separator()

    def launches_loop(self) -> None:
        msg = '\nChoose an action by typing a number and pressing [ENTER]:'
        while True:
            choice = self.ui_manager.ask_user_choice(
                msg, self.launch_choices, ask_exit=True)
            if choice is None:
                self.ui_manager.say('Input was not valid, please'
                                    ' enter a valid number!')
                continue
            filtered = self.launches_menu[choice][1](
                **self.launches_menu[choice][2])
            if len(filtered) < 1:
                self.ui_manager.separator()
                self.ui_manager.say("No launches found!")
                self.ui_manager.separator()
                break
            launch_list_menu = [launch['date_local'].split(
                'T')[0] for launch in filtered]
            msg_launch = 'Choose date by typing number and pressing [ENTER]:'
            choice_launch = self.ui_manager.ask_user_choice(
                msg_launch, launch_list_menu, ask_exit=True)
            if choice_launch is None:
                self.ui_manager.say('Input was not valid, please'
                                    ' enter a valid number!')
            else:
                self.show_single_launch_info(filtered[choice_launch])
                break

    def main_loop(self) -> None:
        """
        Creates an infinite loop until the user or an
        external condition breaks it.
        """
        self.ui_manager.say(self.greeting)
        msg = '\nChoose an action by typing a number and pressing [ENTER]:'
        while True:
            choice = self.ui_manager.ask_user_choice(
                msg, self.main_choices, ask_exit=True)
            if choice is None:
                self.ui_manager.say('Input was not valid, please'
                                    ' enter a valid number!')
                continue
            self.main_menu[choice][1]()
