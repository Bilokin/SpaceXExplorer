from spacexexplorer.info_manager import InfoManager
from spacexexplorer.textui_manager import TextUIManager

from typing import Callable, Any, Optional


class MenuItem(object):
    """Simple Menu Item class"""
    def __init__(self, display_name: str, call_function: Callable, arguments: Optional[dict] = None):
        self.display_name = display_name
        self.call_function = call_function
        self.arguments = arguments or {}
    
    def __call__(self, *args) -> Any:
        return self.call_function(*args, **self.arguments)
    
    def __repr__(self) -> str:
        return self.display_name

class MainManager(object):
    """
    Main manager class that controls the execution loop
    """

    def __init__(self, info_manager: InfoManager, ui_manager: TextUIManager):
        self.info_manager = info_manager
        self.ui_manager = ui_manager
        self.to_exit = False
        self.greeting = "This is a SpaceX info app"
        self.define_menus()

    def define_menus(self):
        self.main_menu = [MenuItem("About company", self.about_info),
                          MenuItem("Browse launches", self.show_launches_menu),
                          MenuItem("Browse launchpads", self.show_launchpads_menu),
                          MenuItem("Browse rockets", self.show_rockets_menu),
                          MenuItem("Show launch statistics", self.show_launch_stats)
                          ]

        self.launches_menu = [
            MenuItem("All", self.info_manager.filter_launches, {}),
            MenuItem("Successful", self.info_manager.filter_launches,
             {"success": True}),
            MenuItem("Failed", self.info_manager.filter_launches,
             {"success": False})
        ]
        for rocket_id in self.info_manager.rocket_info:
            name = self.info_manager.rocket_info[rocket_id]['name']
            item = MenuItem(f"By {name} rocket",
                    self.info_manager.filter_launches,
                    {"rocket": rocket_id})
            self.launches_menu.append(item)
        for launchpad_id in self.info_manager.launchpad_info:
            name = self.info_manager.launchpad_info[launchpad_id]["name"]
            item = MenuItem(f"By {name}",
                    self.info_manager.filter_launches,
                    {"launchpad": launchpad_id})
            self.launches_menu.append(item)


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
    
    def show_launch_stats(self) -> None:
        """
        Prints launch stats
        """
        yearly = sorted([(k, v) for k, v in self.info_manager.launch_stats["years"].items()])
        monthly = sorted([(k, v) for k, v in self.info_manager.launch_stats["months"].items()])
        self.ui_manager.show_launch_stats(yearly, monthly)

    def show_launchpads_menu(self) -> None:
        """
        Prints launchpad menu
        """
        msg = "\nChoose a launchpad by typing a number and pressing [ENTER]:"
        all_lps = self.info_manager.get("launchpads")
        lps_menu = [self.info_manager.launchpad_info[key]["name"]
                    for key in self.info_manager.launchpad_info]
        choice = self.ui_manager.ask_user_choice(
            msg, lps_menu, ask_exit=True)
        if choice is None:
            self.ui_manager.say('Input was not valid, please'
                                ' enter a valid number!')
            return
        for lp in all_lps:
            if lp.get('full_name') == lps_menu[choice]:
                self.ui_manager.show_single_launchpad_info(lp)
                break

    def show_rockets_menu(self) -> None:
        """
        Creates an infinite loop until the user or an
        external condition breaks it.
        """
        msg = '\nChoose a rocket by typing a number and pressing [ENTER]:'
        all_rockets = self.info_manager.get("rockets")
        rockets_menu = [self.info_manager.rocket_info[key]['name']
                        for key in self.info_manager.rocket_info]
        choice = self.ui_manager.ask_user_choice(
            msg, rockets_menu, ask_exit=True)
        if choice is None:
            self.ui_manager.say('Input was not valid, please'
                                ' enter a valid number!')
            return
        for rocket in all_rockets:
            if rocket.get('name') == rockets_menu[choice]:
                extras = self.info_manager.rocket_info[rocket["id"]]
                rocket_successes = extras['successful_launches']
                rocket_total = extras['total_launches']
                rocket_success_rate = None
                if rocket_total > 0:
                    rocket_success_rate = rocket_successes / rocket_total * 100
                self.ui_manager.show_single_rocket_info(rocket, 
                                                            rocket_success_rate=rocket_success_rate)
                break

    def show_launches_menu(self) -> None:
        """
        Creates an infinite loop until the user or an
        external condition breaks it.
        """
        msg = '\nChoose an action by typing a number and pressing [ENTER]:'
        while True:
            choice = self.ui_manager.ask_user_choice(
                msg, self.launches_menu, ask_exit=True)
            if choice is None:
                self.ui_manager.say('Input was not valid, please'
                                    ' enter a valid number!')
                continue
            filtered = self.launches_menu[choice]()
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
                rocket_name = self.info_manager.rocket_info[filtered[choice_launch].get('rocket')]['name']
                self.ui_manager.show_single_launch_info(
                    filtered[choice_launch], rocket_name=rocket_name)
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
                msg, self.main_menu, ask_exit=True)
            if choice is None:
                self.ui_manager.say('Input was not valid, please'
                                    ' enter a valid number!')
                continue
            self.main_menu[choice]()
