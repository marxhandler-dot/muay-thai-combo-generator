# File: mtccg_main_file.py
from colorama import init, Fore, Style
from techniques_browser import technique_details
from technique_customizer import custom_combos
from input_helpers import get_valid_input
from random_combo_generator import training_session
from combo_manager import get_available_savefiles, load_combo_file

init()


def display_loaded_combos(combo_data):
    """Display loaded combinations in a nice format"""
    print(Fore.GREEN + Style.BRIGHT + f"\n === LOADED COMBOS: {combo_data['name']} === " + Style.RESET_ALL)

    combinations = combo_data['combinations']
    colors = [Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.MAGENTA, Fore.BLUE, Fore.WHITE]

    for i, combo in enumerate(combinations):
        colored_combo = []
    for j, technique in enumerate(combo):
        color = colors[j % len(colors)]
        colored_combo.append(color + technique + Style.RESET_ALL)

    print(Fore.RED + Style.BRIGHT + f"Combo {i + 1}: " + Style.RESET_ALL + (
    Fore.WHITE + Style.BRIGHT + " → " + Style.RESET_ALL).join(colored_combo))


def load_saved_combos():
    """Handle the loading of saved combo files"""
    available_files = get_available_savefiles()

    if not available_files:
        print(Fore.YELLOW + " No saved combo files found in the current directory." + Style.RESET_ALL)
        input(Fore.CYAN + "Press Enter to continue..." + Style.RESET_ALL)
        return

    print(Fore.CYAN + Style.BRIGHT + "\n AVAILABLE SAVED COMBOS:" + Style.RESET_ALL)
    for i, filename in enumerate(available_files, 1):
        print(Fore.WHITE + Style.BRIGHT + f"{i}." + Style.RESET_ALL + Fore.YELLOW + f" {filename}" + Style.RESET_ALL)

        print(
 Fore.WHITE + Style.BRIGHT + f"{len(available_files) + 1}." + Style.RESET_ALL + Fore.RED + " Back to Main Menu" + Style.RESET_ALL)

    choice = get_valid_input(
Fore.CYAN + "Select a file to load: " + Style.RESET_ALL,
 1,
 len(available_files) + 1
 )

    if choice == len(available_files) + 1:
        return

    selected_file = available_files[choice - 1]
    combo_data, message = load_combo_file(selected_file)

    if combo_data:
        print(Fore.GREEN + Style.BRIGHT + f" {message}" + Style.RESET_ALL)
        display_loaded_combos(combo_data)

 # Ask user what they want to do next
        while True:
            print(Fore.MAGENTA + Style.BRIGHT + "\nWhat would you like to do?" + Style.RESET_ALL)
            print(
 Fore.WHITE + Style.BRIGHT + "1." + Style.RESET_ALL + Fore.GREEN + " Continue to main difficulty selection" + Style.RESET_ALL)
            print(
 Fore.WHITE + Style.BRIGHT + "2." + Style.RESET_ALL + Fore.BLUE + " Load another combo file" + Style.RESET_ALL)
            print(
 Fore.WHITE + Style.BRIGHT + "3." + Style.RESET_ALL + Fore.RED + " Back to Main Menu" + Style.RESET_ALL)

            next_choice = get_valid_input(Fore.CYAN + "Your choice: " + Style.RESET_ALL, 1, 3)

            if next_choice == 1:
                return # Continue to main menu
            elif next_choice == 2:
                load_saved_combos() # Recursive call to load another file
                return
            elif next_choice == 3:
                return # Back to main menu
    else:
        print(Fore.RED + Style.BRIGHT + f" Error: {message}" + Style.RESET_ALL)
        input(Fore.CYAN + "Press Enter to continue..." + Style.RESET_ALL)


def main():
    print(Fore.CYAN + Style.BRIGHT + """
===WELCOME TO MUAY THAI RANDOM COMBO GENERATOR===""" + Style.RESET_ALL)

 # Main menu with load option
    while True:
        print(Fore.MAGENTA + Style.BRIGHT + "\n MAIN MENU" + Style.RESET_ALL)
        print(
 Fore.WHITE + Style.BRIGHT + "1." + Style.RESET_ALL + Fore.GREEN + " Start Training Session" + Style.RESET_ALL)
        print(Fore.WHITE + Style.BRIGHT + "2." + Style.RESET_ALL + Fore.BLUE + " Load Saved Combos" + Style.RESET_ALL)
        print(Fore.WHITE + Style.BRIGHT + "3." + Style.RESET_ALL + Fore.RED + " Exit" + Style.RESET_ALL)

        main_choice = get_valid_input(Fore.CYAN + "Your choice: " + Style.RESET_ALL, 1, 3)

        if main_choice == 1:
            break # Continue to difficulty selection
        elif main_choice == 2:
            load_saved_combos()
        elif main_choice == 3:
            print(Fore.GREEN + Style.BRIGHT + " Thanks for using the Muay Thai Combo Generator! " + Style.RESET_ALL)
            return "EXIT" # Signal to exit the program

# Existing difficulty selection code
    print(Fore.YELLOW + "Choose your difficulty level:" + Fore.GREEN + Style.BRIGHT +
 "\n(beg)" + Style.RESET_ALL + Fore.YELLOW + "for Beginner techniques and combos." + Fore.RED + Style.BRIGHT +
 "\n(adv)" + Style.RESET_ALL + Fore.YELLOW + "for Advanced techniques and combos." + Style.RESET_ALL)
    print(
 Fore.BLUE + Style.BRIGHT + "(cust)" + Style.RESET_ALL + Fore.YELLOW + "for Customized techniques and combos." + Style.RESET_ALL)

    while True:
        difficulty = (input(Fore.CYAN + "Choose your difficulty option?: " + Style.RESET_ALL))
        if difficulty.lower() == "beg":
            print(Fore.GREEN + Style.BRIGHT + "✓ Beginner mode selected!" + Style.RESET_ALL)
            break

        elif difficulty.lower() == "adv":
            print(Fore.RED + Style.BRIGHT + "✓ Advanced mode selected!" + Style.RESET_ALL)
            break

        elif difficulty.lower() == "cust":
            print(Fore.BLUE + Style.BRIGHT + "✓ Custom mode selected!" + Style.RESET_ALL)
            custom_combos()
            return

        else:
            print(
 Fore.RED + "Invalid Input! Please enter " + Style.BRIGHT + "(beg)" + Style.RESET_ALL + Fore.RED + " for Beginner, " + Style.BRIGHT + "(adv)" + Style.RESET_ALL + Fore.RED + " for Advanced." + Style.RESET_ALL + Fore.RED + Style.BRIGHT + "(cust)" + Style.RESET_ALL + Fore.RED + " for Custom Mode." + Style.RESET_ALL)

 # Existing drill selection code
    while True:
        print(Fore.GREEN + Style.BRIGHT + """
What drills would you like to work on?""" + Style.RESET_ALL)
        print(
 Fore.WHITE + Style.BRIGHT + "1." + Style.RESET_ALL + Fore.MAGENTA + " Random combinations" + Style.RESET_ALL)
        print(
 Fore.WHITE + Style.BRIGHT + "2." + Style.RESET_ALL + Fore.BLUE + " Punches and Elbow only combinations" + Style.RESET_ALL)
        print(
 Fore.WHITE + Style.BRIGHT + "3." + Style.RESET_ALL + Fore.YELLOW + " Kicks and Knee only combinations" + Style.RESET_ALL)
        print(
 Fore.WHITE + Style.BRIGHT + "4." + Style.RESET_ALL + Fore.GREEN + " Punches and Kicks only combinations" + Style.RESET_ALL)
        print(
 Fore.WHITE + Style.BRIGHT + "5." + Style.RESET_ALL + Fore.BLUE + " Knees and Elbows only combinations" + Style.RESET_ALL)
        print(
 Fore.WHITE + Style.BRIGHT + "6." + Style.RESET_ALL + Fore.WHITE + " Fake outs combinations (Only available for Advanced Difficulty)" + Style.RESET_ALL)
        print(
 Fore.WHITE + Style.BRIGHT + "7." + Style.RESET_ALL + Fore.CYAN + " Study technique details" + Style.RESET_ALL)
        print(Fore.WHITE + Style.BRIGHT + "8." + Style.RESET_ALL + Fore.RED + " Back to Main" + Style.RESET_ALL)

        choice = get_valid_input(Fore.CYAN + "What's your choice?: " + Style.RESET_ALL, 1, 8)
        print(Fore.GREEN + Style.BRIGHT + f"✓ Option {choice} selected!" + Style.RESET_ALL)

        if choice == 6:
            if difficulty.lower() == "beg":
                print(
 Fore.YELLOW + Style.BRIGHT + " I'm sorry but this is too advanced for your difficulty. Fundamentals first!" + Style.RESET_ALL)

            else:
                training_session(difficulty, choice)
                break

        elif choice == 7:
            technique_details()
            break

        elif choice == 8:
            return

        else:
            training_session(difficulty, choice)
            break


if __name__ == "__main__":
    while True:
        result = main()
        if result == "EXIT":
            break

        restart = input(
 Fore.MAGENTA + "\nWould you like to return to the main menu? or Exit? " + Style.BRIGHT + "(y/e)" + Style.RESET_ALL + Fore.MAGENTA + ": " + Style.RESET_ALL)
        if restart.lower() != 'y':
            print(
 Fore.GREEN + Style.BRIGHT + " Thanks for training! Keep practicing those combos! " + Style.RESET_ALL)
            break