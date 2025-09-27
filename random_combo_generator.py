# File: random_combo_generator.py
import random
from colorama import init, Fore, Style
from techniques_data import adv_punches, adv_kicks, adv_elbows, adv_knee, beg_punches, beg_kicks, beg_knee, beg_elbows, \
    fake_outs
from input_helpers import get_valid_input
from combo_manager import save_combo, get_save_preferences

init()


def generate_combination(combo_length, difficulty, choice):
    """Generate a single combination and return it"""
    combo = []
    if difficulty.lower() == "beg":
        if choice == 1:
            categories = [beg_punches, beg_kicks, beg_elbows, beg_knee]

        elif choice == 2:
            categories = [beg_punches, beg_elbows]

        elif choice == 4:
            categories = [beg_punches, beg_kicks]

        elif choice == 5:
            categories = [beg_knee, beg_elbows]

        else:
            categories = [beg_kicks, beg_knee]

    else:
        if choice == 1:
            categories = [adv_punches, adv_kicks, adv_elbows, adv_knee, fake_outs]

        elif choice == 2:
            categories = [adv_punches, adv_elbows]

        elif choice == 4:
            categories = [adv_punches, adv_kicks]

        elif choice == 5:
            categories = [adv_knee, adv_elbows]

        elif choice == 6:
            categories = [fake_outs]

        else:
            categories = [adv_kicks, adv_knee]

    for i in range(combo_length):
        chosen_categories = random.choice(categories)
        random_technique = random.choice(chosen_categories)
        combo.append(random_technique)

    return combo


def display_combo(combo, combo_number):
    """Display a single combination with colors"""
    colored_combo = []
    colors = [Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.MAGENTA, Fore.BLUE, Fore.WHITE]
    for i, technique in enumerate(combo):
        color = colors[i % len(colors)]
        colored_combo.append(color + technique + Style.RESET_ALL)

    print(Fore.RED + Style.BRIGHT + f"Combo {combo_number}: " + Style.RESET_ALL + (
            Fore.WHITE + Style.BRIGHT + " → " + Style.RESET_ALL).join(colored_combo))


def training_session(difficulty, choice):
    """Generate training combinations with option to save"""
    num_combos = get_valid_input(
        Fore.CYAN + "How many different combinations do you want to practice?: " + Style.RESET_ALL, 1, 10,
        Fore.YELLOW + "Don't be lazy! Enter at least 1 combination." + Style.RESET_ALL,
        Fore.YELLOW + "Easy now! Max 10 combinations please." + Style.RESET_ALL)
    combo_length = get_valid_input(Fore.CYAN + "How many techniques per combo?: " + Style.RESET_ALL, 1, 8,
                                   Fore.YELLOW + "Don't be lazy! Enter at least 1 technique." + Style.RESET_ALL,
                                   Fore.YELLOW + "Easy! Max 8 techniques please." + Style.RESET_ALL)

    print(Fore.GREEN + Style.BRIGHT + f"\n🥊 ---Training Session: {num_combos} combinations ---" + Style.RESET_ALL)

    # Store all generated combinations
    all_combinations = []

    for i in range(num_combos):
        combo = generate_combination(combo_length, difficulty, choice)
        all_combinations.append(combo)
        display_combo(combo, i + 1)

    # Ask if user wants to save the combinations
    preferences = get_save_preferences()
    if preferences['should_save']:
        success, message = save_combo(all_combinations, preferences['combo_name'], preferences['filename'])
        if success:
            print(Fore.GREEN + Style.BRIGHT + message + Style.RESET_ALL)
        else:
            print(Fore.RED + Style.BRIGHT + message + Style.RESET_ALL)