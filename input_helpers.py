#File name input_helpers.py
from colorama import init, Fore, Style
init()

def get_valid_input(prompt, min_value, max_value, too_low_msg=None, too_high_msg=None, invalid_msg=None):
    while True:
        try:
            choice = int(input(prompt))
            if choice > max_value:
                if too_high_msg is not None:
                    print(too_high_msg)
                else:
                    print(Fore.RED +
                        f"Sorry! There are no options beyond {max_value}, Please choose within the available options."+ Style.RESET_ALL)
            elif choice < min_value:
                if too_low_msg is not None:
                    print(too_low_msg)
                else:
                    print(Fore.RED + "Invalid Input! Please choose within the available options."+ Style.RESET_ALL)
            else:
                break
        except ValueError:
            if invalid_msg is not None:
                print(invalid_msg)
            else:
                print(Fore.RED + "Invalid Input! Please enter a valid number." + Style.RESET_ALL)
    return choice