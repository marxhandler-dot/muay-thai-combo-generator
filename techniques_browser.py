#File name techniques_browser.py
import math
from colorama import init, Fore, Style
from techniques_data import technique_info
init()


def search_techniques(search_term):
    matches = []

    for techniques in technique_info:
        if search_term.lower() in techniques['name'].lower():
            matches.append(techniques['name'])
    return matches

def technique_details():
    print(
 Fore.YELLOW + Style.BRIGHT + " Disclaimer!" + Style.RESET_ALL + Fore.YELLOW + " The tips being provided here is just a general idea on how to perform or execute the techniques,\nYou can use other sources for more depth and information on the technique." + Style.RESET_ALL)
    while True:
        print(Fore.MAGENTA + Style.BRIGHT + """
How would you like to find techniques?""" + Style.RESET_ALL)
        print(Fore.WHITE + Style.BRIGHT + "1." + Style.RESET_ALL + Fore.CYAN + " Browse by page?" + Style.RESET_ALL)
        print(
 Fore.WHITE + Style.BRIGHT + "2." + Style.RESET_ALL + Fore.GREEN + " Search by name?" + Style.RESET_ALL)
        print(Fore.WHITE + Style.BRIGHT + "3." + Style.RESET_ALL + Fore.RED + " Exit" + Style.RESET_ALL)

        user_pick = input(Fore.CYAN + "Your choice: " + Style.RESET_ALL)

        if user_pick == "1":
            current_page = 1
            techniques_per_page = 10
            total_techniques = len(technique_info)

            while True:
                start_index = (current_page - 1) * techniques_per_page
                end_index = start_index + techniques_per_page

                current_page_techniques = technique_info[start_index: end_index]
                print(Fore.CYAN + Style.BRIGHT + f"\n PAGE: {current_page}" + Style.RESET_ALL)

                for i, technique in enumerate(current_page_techniques):
                    display_number = start_index + i + 1
                    print(
 Fore.WHITE + Style.BRIGHT + f"{display_number}." + Style.RESET_ALL + Fore.YELLOW + f" {technique['name']}" + Style.RESET_ALL)

                print(Fore.GREEN + Style.BRIGHT + "\nOptions:" + Style.RESET_ALL)
                print(Fore.BLUE + "n" + Style.RESET_ALL + " - Next page")
                print(Fore.BLUE + "p" + Style.RESET_ALL + " - Previous page")
                print(Fore.MAGENTA + "To choose" + Style.RESET_ALL + " = Enter technique number")
                print(Fore.RED + "q" + Style.RESET_ALL + " - Quit")

                user_choice = input(Fore.CYAN + "Your choice: " + Style.RESET_ALL)

                if user_choice.lower() == "n":
                    max_pages = math.ceil(total_techniques / techniques_per_page)
                    if current_page < max_pages:
                        current_page += 1

                    else:
                        print(Fore.YELLOW + "You're already in the last page!" + Style.RESET_ALL)

                elif user_choice.lower() == "p":
                        if current_page > 1:
                            current_page -= 1

                        else:
                            print(Fore.YELLOW + "You're already in the first page!" + Style.RESET_ALL)

                elif user_choice.isdigit():
                    selected_number = int(user_choice)

                    if selected_number in range(1, total_techniques + 1):
                        actual_index = selected_number - 1
                        selected_technique = technique_info[actual_index]
                        print(
 Fore.GREEN + Style.BRIGHT + f"\n Name: " + Style.RESET_ALL + Fore.CYAN + f"{selected_technique['name']}" + Style.RESET_ALL)
                        print(
 Fore.BLUE + Style.BRIGHT + " Description: " + Style.RESET_ALL + Fore.WHITE + f"{selected_technique['description']}" + Style.RESET_ALL)
                        print(
 Fore.YELLOW + Style.BRIGHT + " Tip: " + Style.RESET_ALL + Fore.GREEN + f"{selected_technique['tip']}" + Style.RESET_ALL)

                    else:
                        print(Fore.RED + "Invalid technique number! Please try again." + Style.RESET_ALL)

                elif user_choice.lower() in ['q', 'quit']:
                    break

                else:
                    print(Fore.RED + "Error! Invalid Input!" + Style.RESET_ALL)

        elif user_pick == "2":
            search_term = input(Fore.CYAN + "Technique name here: " + Style.RESET_ALL)
            matches = search_techniques(search_term)

            if matches:
                print(Fore.GREEN + f"\n✓ Found {len(matches)} matches:" + Style.RESET_ALL)
                for i, match in enumerate(matches, 1):
                    print(
 Fore.WHITE + Style.BRIGHT + f"{i}." + Style.RESET_ALL + Fore.YELLOW + f" {match}" + Style.RESET_ALL)
                try:
                    selected = int(input(Fore.CYAN + "Select technique number: " + Style.RESET_ALL))
                    if 1 <= selected <= len(matches):
                        selected_technique_name = matches[selected - 1]
                        selected_technique = None

                        for technique in technique_info:
                            if technique['name'] == selected_technique_name:
                                selected_technique = technique
                                break

                        if selected_technique:
                            print(
                        Fore.GREEN + Style.BRIGHT + f"\n🥊 Name: " + Style.RESET_ALL + Fore.CYAN + f"{selected_technique['name']}" + Style.RESET_ALL)
                            print(
                        Fore.BLUE + Style.BRIGHT + "📝 Description: " + Style.RESET_ALL + Fore.WHITE + f"{selected_technique['description']}" + Style.RESET_ALL)
                            print(
                        Fore.YELLOW + Style.BRIGHT + "💡 Tip: " + Style.RESET_ALL + Fore.GREEN + f"{selected_technique['tip']}" + Style.RESET_ALL)
                        else:
                            print(Fore.RED + "Technique not found!" + Style.RESET_ALL)

                    else:
                        print(Fore.RED + "Invalid selection number!" + Style.RESET_ALL)

                except ValueError:
                    print(Fore.RED + "Please enter a valid number!" + Style.RESET_ALL)

            else:
                print(Fore.RED + "❌ No matches found!" + Style.RESET_ALL)

        elif user_pick == "3":
            print(Fore.GREEN + "Thanks for studying! Keep practicing! 🥊" + Style.RESET_ALL)
            break

        else:
            print(Fore.RED + "Invalid Input!" + Style.RESET_ALL)