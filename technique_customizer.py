#File: technique_customizer.py
import random
from colorama import init, Fore, Style
from techniques_data import specific_category_mapping, random_category_mapping
from input_helpers import get_valid_input
from combo_manager import save_combo, get_save_preferences
init()


def custom_combos():
    cust_combo = get_valid_input(Fore.CYAN + Style.BRIGHT + "How many combos do you want?: " + Style.RESET_ALL, 1, 10,
 Fore.YELLOW + "Don't be lazy! Enter at least 1 combination." + Style.RESET_ALL,
 Fore.YELLOW + "Easy now! Max 10 combinations please." + Style.RESET_ALL)
    cust_techniques = get_valid_input(Fore.CYAN + Style.BRIGHT + "How many techniques per combo?: " + Style.RESET_ALL,
 1, 8,
 Fore.YELLOW + "Don't be lazy! Enter at least 1 technique." + Style.RESET_ALL,
 Fore.YELLOW + "Easy! Max 8 techniques please." + Style.RESET_ALL)

    all_customizations = []
    saved_result_combo = []
    for combo_num in range(cust_combo):
        single_combo_custom = []
        for technique_pos in range(cust_techniques):
            while True:
                    try:
                        print(Fore.GREEN + Style.BRIGHT + "\n CUSTOMIZATION OPTIONS:" + Style.RESET_ALL)
                        print(
 Fore.WHITE + Style.BRIGHT + "1." + Style.RESET_ALL + Fore.MAGENTA + " Add specific technique" + Style.RESET_ALL)
                        print(
 Fore.WHITE + Style.BRIGHT + "2." + Style.RESET_ALL + Fore.BLUE + " Add a random technique" + Style.RESET_ALL)
                        print(
 Fore.WHITE + Style.BRIGHT + "3." + Style.RESET_ALL + Fore.RED + " Back to Main Menu." + Style.RESET_ALL)

                        print(
 Fore.YELLOW + Style.BRIGHT + f" Combo {combo_num + 1} | Technique position {technique_pos + 1}" + Style.RESET_ALL)
                        cust_choice = int(input(Fore.CYAN + "Your choice: " + Style.RESET_ALL))

                        if cust_choice == 1:
                            print(Fore.GREEN + Style.BRIGHT + "\n SELECT TECHNIQUE CATEGORY:" + Style.RESET_ALL)
                            print(
 Fore.WHITE + Style.BRIGHT + "1." + Style.RESET_ALL + Fore.RED + " Punches" + Style.RESET_ALL)
                            print(
 Fore.WHITE + Style.BRIGHT + "2." + Style.RESET_ALL + Fore.YELLOW + " Kicks" + Style.RESET_ALL)
                            print(
 Fore.WHITE + Style.BRIGHT + "3." + Style.RESET_ALL + Fore.MAGENTA + " Elbows" + Style.RESET_ALL)
                            print(
 Fore.WHITE + Style.BRIGHT + "4." + Style.RESET_ALL + Fore.BLUE + " Knees" + Style.RESET_ALL)
                            print(Fore.WHITE + Style.BRIGHT + "5." + Style.RESET_ALL + Fore.WHITE + " Fakes & Feints" + Style.RESET_ALL)

                            category_choice = int(input(Fore.CYAN + "Pick category: " + Style.RESET_ALL))

                            if category_choice == 1:
                                print(Fore.RED + Style.BRIGHT + "\n AVAILABLE PUNCHES:" + Style.RESET_ALL)
                                for i, punch in enumerate(specific_category_mapping["specific_punches"], 1):
                                    print(
 Fore.WHITE + Style.BRIGHT + f"{i}." + Style.RESET_ALL + Fore.YELLOW + f" {punch}" + Style.RESET_ALL)
                                technique_choice = int(input(Fore.CYAN + "Pick technique: " + Style.RESET_ALL))
                                if 1 <= technique_choice <= len(specific_category_mapping["specific_punches"]):
                                    selected_technique = specific_category_mapping["specific_punches"][technique_choice - 1]
                                    single_combo_custom.append(selected_technique)
                                    print(
 Fore.GREEN + Style.BRIGHT + " " + Style.RESET_ALL + Fore.WHITE + f"{selected_technique}" + Style.RESET_ALL + Fore.GREEN + f" has been added to Combo {combo_num + 1}, Technique Position {technique_pos + 1}" + Style.RESET_ALL)
                                    break
                                else:
                                    print(Fore.RED + "Invalid selection! Please try again." + Style.RESET_ALL)
                                    continue

                            elif category_choice == 2:
                                print(Fore.YELLOW + Style.BRIGHT + "\n AVAILABLE KICKS:" + Style.RESET_ALL)
                                for i, kick in enumerate(specific_category_mapping["specific_kicks"], 1):
                                    print(
 Fore.WHITE + Style.BRIGHT + f"{i}." + Style.RESET_ALL + Fore.CYAN + f" {kick}" + Style.RESET_ALL)
                                technique_choice = int(input(Fore.CYAN + "Pick technique: " + Style.RESET_ALL))
                                if 1 <= technique_choice <= len(specific_category_mapping["specific_kicks"]):
                                    selected_technique = specific_category_mapping["specific_kicks"][technique_choice - 1]
                                    single_combo_custom.append(selected_technique)
                                    print(
 Fore.GREEN + Style.BRIGHT + " " + Style.RESET_ALL + Fore.WHITE + f"{selected_technique}" + Style.RESET_ALL + Fore.GREEN + f" has been added to Combo {combo_num + 1}, Technique Position {technique_pos + 1}" + Style.RESET_ALL)
                                    break
                                else:
                                    print(Fore.RED + "Invalid selection! Please try again." + Style.RESET_ALL)
                                    continue

                            elif category_choice == 3:
                                print(Fore.MAGENTA + Style.BRIGHT + "\n AVAILABLE ELBOWS:" + Style.RESET_ALL)
                                for i, elbow in enumerate(specific_category_mapping["specific_elbows"], 1):
                                    print(
 Fore.WHITE + Style.BRIGHT + f"{i}." + Style.RESET_ALL + Fore.GREEN + f" {elbow}" + Style.RESET_ALL)
                                technique_choice = int(input(Fore.CYAN + "Pick technique: " + Style.RESET_ALL))
                                if 1 <= technique_choice <= len(specific_category_mapping["specific_elbows"]):
                                    selected_technique = specific_category_mapping["specific_elbows"][technique_choice - 1]
                                    single_combo_custom.append(selected_technique)
                                    print(
 Fore.GREEN + Style.BRIGHT + " " + Style.RESET_ALL + Fore.WHITE + f"{selected_technique}" + Style.RESET_ALL + Fore.GREEN + f" has been added to Combo {combo_num + 1}, Technique Position {technique_pos + 1}" + Style.RESET_ALL)
                                    break

                                else:
                                    print(Fore.RED + "Invalid selection! Please try again." + Style.RESET_ALL)
                                    continue

                            elif category_choice == 4:
                                print(Fore.BLUE + Style.BRIGHT + "\n AVAILABLE KNEES:" + Style.RESET_ALL)
                                for i, knee in enumerate(specific_category_mapping["specific_knees"], 1):
                                    print(
 Fore.WHITE + Style.BRIGHT + f"{i}." + Style.RESET_ALL + Fore.MAGENTA + f" {knee}" + Style.RESET_ALL)
                                technique_choice = int(input(Fore.CYAN + "Pick technique: " + Style.RESET_ALL))
                                if 1 <= technique_choice <= len(specific_category_mapping["specific_knees"]):
                                    selected_technique = specific_category_mapping["specific_knees"][technique_choice - 1]
                                    single_combo_custom.append(selected_technique)
                                    print(
 Fore.GREEN + Style.BRIGHT + " " + Style.RESET_ALL + Fore.WHITE + f"{selected_technique}" + Style.RESET_ALL + Fore.GREEN + f" has been added to Combo {combo_num + 1}, Technique Position {technique_pos + 1}" + Style.RESET_ALL)
                                    break
                                else:
                                    print(Fore.RED + "Invalid selection! Please try again." + Style.RESET_ALL)
                                    continue

                            elif category_choice == 5:
                                print(Fore.BLUE + Style.BRIGHT + "\n AVAILABLE FAKES:" + Style.RESET_ALL)
                                for i, fake in enumerate(specific_category_mapping["specific_fake_feints"], 1):
                                    print(
 Fore.WHITE + Style.BRIGHT + f"{i}." + Style.RESET_ALL + Fore.MAGENTA + f" {fake}" + Style.RESET_ALL)
                                technique_choice = int(input(Fore.CYAN + "Pick technique: " + Style.RESET_ALL))
                                if 1 <= technique_choice <= len(specific_category_mapping["specific_fake_feints"]):
                                    selected_technique = specific_category_mapping["specific_fake_feints"][
                                    technique_choice - 1]
                                    single_combo_custom.append(selected_technique)
                                    print(
 Fore.GREEN + Style.BRIGHT + " " + Style.RESET_ALL + Fore.WHITE + f"{selected_technique}" + Style.RESET_ALL + Fore.GREEN + f" has been added to Combo {combo_num + 1}, Technique Position {technique_pos + 1}" + Style.RESET_ALL)
                                    break
                                else:
                                    print(Fore.RED + "Invalid selection! Please try again." + Style.RESET_ALL)
                                    continue
                            else:
                                print(Fore.RED + Style.BRIGHT + " Invalid choice!" + Style.RESET_ALL)

                        elif cust_choice == 2:
                            print(Fore.BLUE + Style.BRIGHT + "\n RANDOM TECHNIQUE CATEGORIES:" + Style.RESET_ALL)
                            print(
 Fore.WHITE + Style.BRIGHT + "1." + Style.RESET_ALL + Fore.RED + " Random Punches" + Style.RESET_ALL)
                            print(
 Fore.WHITE + Style.BRIGHT + "2." + Style.RESET_ALL + Fore.YELLOW + " Random Kicks" + Style.RESET_ALL)
                            print(
 Fore.WHITE + Style.BRIGHT + "3." + Style.RESET_ALL + Fore.MAGENTA + " Random Elbows" + Style.RESET_ALL)
                            print(
 Fore.WHITE + Style.BRIGHT + "4." + Style.RESET_ALL + Fore.BLUE + " Random Knees" + Style.RESET_ALL)
                            print(Fore.WHITE + Style.BRIGHT + "5." + Style.RESET_ALL + Fore.WHITE + " Random Fakes & Feints" + Style.RESET_ALL)

                            random_choice = int(input(Fore.CYAN + "Pick random category: " + Style.RESET_ALL))

                            if random_choice == 1:
                                single_combo_custom.append("random_punches")
                                print(
 Fore.GREEN + Style.BRIGHT + " " + Style.RESET_ALL + Fore.RED + " A random punch" + Style.RESET_ALL + Fore.GREEN + f" has been added to Combo {combo_num + 1}, Technique Position {technique_pos + 1}" + Style.RESET_ALL)
                                break
                            elif random_choice == 2:
                                single_combo_custom.append("random_kicks")
                                print(
 Fore.GREEN + Style.BRIGHT + " " + Style.RESET_ALL + Fore.YELLOW + " A random kick" + Style.RESET_ALL + Fore.GREEN + f" has been added to Combo {combo_num + 1}, Technique Position {technique_pos + 1}" + Style.RESET_ALL)
                                break
                            elif random_choice == 3:
                                single_combo_custom.append("random_elbows")
                                print(
 Fore.GREEN + Style.BRIGHT + " " + Style.RESET_ALL + Fore.MAGENTA + " A random elbow" + Style.RESET_ALL + Fore.GREEN + f" has been added to Combo {combo_num + 1}, Technique Position {technique_pos + 1}" + Style.RESET_ALL)
                                break
                            elif random_choice == 4:
                                single_combo_custom.append("random_knees")
                                print(
 Fore.GREEN + Style.BRIGHT + " " + Style.RESET_ALL + Fore.BLUE + " A random knee" + Style.RESET_ALL + Fore.GREEN + f" has been added to Combo {combo_num + 1}, Technique Position {technique_pos + 1}" + Style.RESET_ALL)
                                break
                            elif random_choice == 5:
                                single_combo_custom.append("random_fake_feints")
                                print(
 Fore.GREEN + Style.BRIGHT + " " + Style.RESET_ALL + Fore.BLUE + " A random fake" + Style.RESET_ALL + Fore.GREEN + f" has been added to Combo {combo_num + 1}, Technique Position {technique_pos + 1}" + Style.RESET_ALL)
                                break

                            else:
                                print(Fore.RED + Style.BRIGHT + " Invalid choice!" + Style.RESET_ALL)

                        elif cust_choice == 3:
                            return

                        else:
                            print(
 Fore.RED + Style.BRIGHT + " Error! Please select from available options." + Style.RESET_ALL)

                    except ValueError:
                        print(Fore.RED + Style.BRIGHT + " Invalid Input!" + Style.RESET_ALL)

        all_customizations.append(single_combo_custom)

        print(Fore.GREEN + Style.BRIGHT + "\n === CUSTOM COMBINATIONS GENERATED === " + Style.RESET_ALL)
        for i, customized_combo in enumerate(all_customizations):
            result_combo = []
            for item in customized_combo:
                if item in random_category_mapping:
                    technique = random.choice(random_category_mapping[item])
                    result_combo.append(technique)
                else:
                    result_combo.append(item)

            saved_result_combo.append(result_combo)

            colored_combo = []
            colors = [Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.MAGENTA, Fore.BLUE, Fore.WHITE]
            for item, technique in enumerate(result_combo):
                color = colors[i % len(colors)]
                colored_combo.append(color + technique + Style.RESET_ALL)

                print(Fore.RED + Style.BRIGHT + f"Custom Combination {i + 1}: " + Style.RESET_ALL + (
 Fore.WHITE + Style.BRIGHT + " → " + Style.RESET_ALL).join(colored_combo))

    preferences = get_save_preferences()
    if preferences['should_save']:
        success, message = save_combo(saved_result_combo, preferences['combo_name'], preferences['filename'])
        if success:
            print(Fore.GREEN + Style.BRIGHT + message + Style.RESET_ALL)
        else:
            print(Fore.RED + Style.BRIGHT + message + Style.RESET_ALL)