import os
import sys


class TextUIManager():
    """
    Class that interacts with the user.
    """

    def __init__(self):
        """
        Constructor method.
        """
        self.column_limit = 10
        self.month_names = ["Jan", "Feb", "Mar",
                            "Apl", "May", "Jun",
                            "Jul", "Aug", "Sep",
                            "Oct", "Nov", "Dec"]

    def clear(self) -> None:
        """
        Clears the terminal
        """
        os.system('cls||clear')

    def say(self, message: str) -> None:
        """
        Prints a message.
        """
        print(message)

    def separator(self) -> None:
        """
        Prints a separator.
        """
        print('=============================================')

    def ask_continue_or_exit(self) -> bool:
        """
        Asks user if we want to continue the main loop
        """
        self.say("To continue press Enter, to exit please type 'e'")
        answer = input()
        if answer == 'e':
            sys.exit('Bye!')
        return True
    
    def show_launch_stats(self, yearly: list, monthly: list) -> None:
        """
        Prints launch stats
        """
        self.say("Statistics by years:")
        title_row = "|"
        value_row = "|"
        for year, val in yearly:
            title_row += str(year) + "|"
            value_row += str(val).ljust(4) + "|"
        self.say(title_row)
        self.say(value_row)
        self.say("Statistics by months:")
        title_row = "|"
        value_row = "|"
        for month, val in monthly:
            title_row += str(self.month_names[month-1]).ljust(4) + "|"
            value_row += str(val).ljust(4) + "|"
        self.say(title_row)
        self.say(value_row)

    def show_single_launchpad_info(self, launchpad: dict, **extra_info) -> None:
        """
        Prints a single launchpad info
        """
        self.separator()
        self.say("Launchpad information")
        self.separator()
        properties = ['full_name', 'locality',
                      'region', 'status',
                      'launch_successes', 'launch_attempts',
                      'details'
                      ]
        for prop in properties:
            self.say(
                f"{prop.capitalize().replace('_', ' ')}: {launchpad.get(prop)}")
        self.separator()

    def show_single_rocket_info(self, rocket: dict, **extra_info) -> None:
        """
        Prints a signal rocket info
        """
        self.separator()
        self.say("Rocket information")
        self.separator()
        properties = ['name', 'type',
                      'active', 'stages',
                      'description']
        for prop in properties:
            self.say(
                f"{prop.capitalize().replace('_', ' ')}: {rocket.get(prop)}")
        rocket_success_rate = extra_info.get("rocket_success_rate")
        if rocket_success_rate:
            self.say(f"Rocket success rate: {rocket_success_rate: 0.1f}%")
        self.separator()

    def show_single_launch_info(self, launch: dict, **extra_info) -> None:
        """
        Prints a single launch info
        """
        properties = ['date_local', 'flight_number',
                      'name', 'success', 'reused',
                      'landing_success',  'details']
        self.separator()
        self.say("Launch information")
        self.separator()
        rocket_name = extra_info.get("rocket_name")
        if rocket_name:
            self.say(f"Rocket: {rocket_name}")
        for prop in properties:
            self.say(
                f"{prop.capitalize().replace('_', ' ')}: {launch.get(prop)}")
        
        self.separator()

    def ask_user_choice(self, message: str, mlist: list, default: int = -1,
                        ask_exit: bool = False):
        """
        Asks user to choose the value among the proposed ones.
        """
        list_length = len(mlist)
        while True:
            self.say(message)
            # single column print:
            if (len(mlist) < self.column_limit):
                for item, iteration in zip(mlist, range(0, list_length)):
                    if iteration == default:
                        self.say(f'{iteration}: {item} [default]')
                        continue
                    self.say(f'{iteration}: {item}')
            else:  # three column print
                strlist = []
                for i in range(0, list_length):
                    if default > -1 and i == default:
                        strlist += [f'{i}: {mlist[i]} [default]']
                        continue
                    strlist += [f'{i}: {mlist[i]}']
                strlist = self.add_spaces(strlist)
                for a, b, c in zip(strlist[::3], strlist[1::3], strlist[2::3]):
                    print('{}{}{}'.format(a, b, c))
                if (len(strlist) % 3 == 1):
                    print(strlist[-1])
                if (len(strlist) % 3 == 2):
                    print('{}{}'.format(strlist[-2], strlist[-1]))
            if ask_exit:
                self.say("To exit: please type 'e'")
            answer = input()
            if self.is_int(answer):
                if int(answer) < list_length:
                    return int(answer)
            if not answer and default > -1:
                return default
            if answer == 'e':
                sys.exit('Bye!')
            return None

    def add_spaces(self, strlist: list) -> list:
        """
        Adds spaces to make columns.
        """
        maxlen = len(max(strlist, key=len)) + 1
        return [s.ljust(maxlen) for s in strlist]

    def is_int(self, s: str) -> bool:
        """
        Returns True if argument is integer.
        """
        try:
            int(s)
            return True
        except ValueError:
            return False
