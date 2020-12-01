"""An example program to show biases in AI training techniques, using lists of letters."""

# imports:
import termios, sys, tty, csv, random, time
from threading import Timer
from prettytable import PrettyTable

class color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def main():
    print(
        "\n---------------------------------------------\n|\t\t\t\t\t    |\n|"
        + color.BOLD
        + color.GREEN
        + "  Welcome to the QAZPLM Training Program!  "
        + color.END
        + color.END
        + "|\n|\t\t\t\t\t    |\n---------------------------------------------\n"
    )

    print(
        color.BOLD
        + color.UNDERLINE
        + "About This Program:"
        + color.END
        + color.END
        + "  This is a training algorithm that is used to analyze subconcious user bias. The program will ask the user to enter as many letters as possible for 15 second trials, then analyze and create a dataset trained off of user entries. There will be 4 Trials, amounting to the user entering letters for 60 seconds in total.\n\nThe program will now ask you to enter as many letters as you can for 15 seconds. Note! You are not entering words, just keys randomly! Keys considered to be on the left side of the keyboard are QWASZXE, the middle DCRFVTGBYHU, and the right is POLMKNIJ."
    )
    user_ready = 0
    letter_input = []
    trial_count = 1
    all_inputted_letters = []
    trials_list = []

    user_name = input(color.BOLD + color.UNDERLINE + "\nInput your name:" + color.END + color.END + " ")

    user_hand = input(color.BOLD + color.UNDERLINE + "\nInput right if you are right-handed and left if you are left-handed:" + color.END + color.END + " ")

    print("\nYou may continue when you are ready.")
    while trial_count <= 4:
        user_ready = "N"
        if trial_count == 1:
            while user_ready != "Y":
                user_ready = input(
                    color.UNDERLINE
                    + "\nEnter Y when you are ready to continue:"
                    + color.END
                    + "  "
                )
        else:
            user_ready = input(
                color.UNDERLINE
                + "\nEnter V to view Trial Results. Enter Y if you are ready to continue:"
                + color.END
                + "  "
            )
            if user_ready == "Y":
                pass
            elif user_ready == "V":
                print(trial_table)
                while user_ready != "Y":
                    user_ready = input(
                        color.UNDERLINE
                        + "\nEnter Y when you are ready to continue:"
                        + color.END
                        + "  "
                    )
            else:
                while user_ready != "Y":
                    user_ready = input(
                        "\nEnter Y when you are ready to continue:" + color.END + "  "
                    )

        letter_input = user_input()
        all_inputted_letters = all_inputted_letters + letter_input
        length = len(letter_input)

        counted_letters = count_letters(length, letter_input)
        trial_dict, trial_table = data_center(user_hand, trial_count, length, counted_letters, user_name)
        trials_list.append(trial_dict)

        if trial_count < 4:
            print(
                "Trial #",
                trial_count,
                " completed! Let the program know when you are ready to run another trial.",
            )
        else:
            print("Trials complete!")
        trial_count += 1

    table = PrettyTable()
    table.field_names = [
        "Trial #",
        "Total Letter Count",
        "Left %",
        "Middle %",
        "Right %",
        "Correct",
        "Actual Handedness",
    ]

    total_length = len(all_inputted_letters)
    all_counted_letters = count_letters(total_length, all_inputted_letters)
    trial = "Total"
    total_trials_dict, total_trial_table = data_center(user_hand,
        trial, total_length, all_counted_letters, user_name
    )

    trials_list.append(total_trials_dict)

    print("\n\n\n\nGENERATING DATASET ........")
    generated_input_data = generate_dataset(total_length, all_inputted_letters)
    gen_length = len(generated_input_data)

    gen_counted_letters = count_letters(gen_length, generated_input_data)

    trial = "Generated Data"
    gen_trials_dict, gen_trial_table = data_center(
        user_hand, trial, gen_length, gen_counted_letters, user_name
    )
    trials_list.append(gen_trials_dict)

    user_ready = input(
        color.UNDERLINE
        + "\nEnter V to view Generated Results. Enter Y if you are ready to continue:"
        + color.END
        + "  "
    )
    if user_ready == "Y":
        pass
    elif user_ready == "V":
        print(gen_trial_table)
        while user_ready != "Y":
            user_ready = input(
                color.UNDERLINE
                + "\nEnter Y when you are ready to continue:"
                + color.END
                + "  "
            )
    else:
        while user_ready != "Y":
            user_ready = input(
                color.UNDERLINE
                + "\nEnter Y when you are ready to continue:"
                + color.END
                + "  "
            )

    test_list = trials_list[0:4]
    # write all results to CSV
    keys = trials_list[0].keys()
    with open("results.csv", "w", newline="") as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writerows(test_list)

    for trial_dict in trials_list:
        table.add_row(
            [
                trial_dict["trial"],
                trial_dict["length"],
                trial_dict["left_percent"],
                trial_dict["middle_percent"],
                trial_dict["right_percent"],
                trial_dict["correct"],
                trial_dict["actual_handedness"]
            ]
        )

    print(table)

    user_ready = input(
        color.UNDERLINE
        + "\nEnter C to import a CSV file for further analysis. Enter N to exit the program:"
        + color.END
        + "  "
    )
    if user_ready == "N":
        pass
    elif user_ready == "C":
        analysis(trials_list[0:4])
    else:
        while user_ready != "Y":
            user_ready = input(
                color.UNDERLINE
                + "\nEnter Y to exit the program:"
                + color.END
                + "  "
            )



def generate_dataset(total_length, all_inputted_letters):
    length = total_length

    generated_data = []
    i = 0

    while i < length:
        current_random = random.choice(all_inputted_letters)
        generated_data.append(current_random)
        i += 1

    return generated_data


def count_letters(length, letter_input):
    letter_list = []
    total = length

    a_count = letter_input.count("a")
    a_dict = {"letter": "a", "count": a_count, "percent": ((a_count / total) * 100)}
    letter_list.append(a_dict)

    b_count = letter_input.count("b")
    b_dict = {"letter": "b", "count": b_count, "percent": ((b_count / total) * 100)}
    letter_list.append(b_dict)

    c_count = letter_input.count("c")
    c_dict = {"letter": "c", "count": c_count, "percent": ((c_count / total) * 100)}
    letter_list.append(c_dict)

    d_count = letter_input.count("d")
    d_dict = {"letter": "d", "count": d_count, "percent": ((d_count / total) * 100)}
    letter_list.append(d_dict)

    e_count = letter_input.count("e")
    e_dict = {"letter": "e", "count": e_count, "percent": ((e_count / total) * 100)}
    letter_list.append(e_dict)

    f_count = letter_input.count("f")
    f_dict = {"letter": "f", "count": f_count, "percent": ((f_count / total) * 100)}
    letter_list.append(f_dict)

    g_count = letter_input.count("g")
    g_dict = {"letter": "g", "count": g_count, "percent": ((g_count / total) * 100)}
    letter_list.append(g_dict)

    h_count = letter_input.count("h")
    h_dict = {"letter": "h", "count": h_count, "percent": ((h_count / total) * 100)}
    letter_list.append(h_dict)

    i_count = letter_input.count("i")
    i_dict = {"letter": "i", "count": i_count, "percent": ((i_count / total) * 100)}
    letter_list.append(i_dict)

    j_count = letter_input.count("j")
    j_dict = {"letter": "j", "count": j_count, "percent": ((j_count / total) * 100)}
    letter_list.append(j_dict)

    k_count = letter_input.count("k")
    k_dict = {"letter": "k", "count": k_count, "percent": ((k_count / total) * 100)}
    letter_list.append(k_dict)

    l_count = letter_input.count("l")
    l_dict = {"letter": "l", "count": l_count, "percent": ((l_count / total) * 100)}
    letter_list.append(l_dict)

    m_count = letter_input.count("m")
    m_dict = {"letter": "m", "count": m_count, "percent": ((m_count / total) * 100)}
    letter_list.append(m_dict)

    n_count = letter_input.count("n")
    n_dict = {"letter": "n", "count": n_count, "percent": ((n_count / total) * 100)}
    letter_list.append(n_dict)

    o_count = letter_input.count("o")
    o_dict = {"letter": "o", "count": o_count, "percent": ((o_count / total) * 100)}
    letter_list.append(o_dict)

    p_count = letter_input.count("p")
    p_dict = {"letter": "p", "count": p_count, "percent": ((p_count / total) * 100)}
    letter_list.append(p_dict)

    q_count = letter_input.count("q")
    q_dict = {"letter": "q", "count": q_count, "percent": ((q_count / total) * 100)}
    letter_list.append(q_dict)

    r_count = letter_input.count("r")
    r_dict = {"letter": "r", "count": r_count, "percent": ((r_count / total) * 100)}
    letter_list.append(r_dict)

    s_count = letter_input.count("s")
    s_dict = {"letter": "s", "count": s_count, "percent": ((s_count / total) * 100)}
    letter_list.append(s_dict)

    t_count = letter_input.count("t")
    t_dict = {"letter": "t", "count": t_count, "percent": ((t_count / total) * 100)}
    letter_list.append(t_dict)

    u_count = letter_input.count("u")
    u_dict = {"letter": "u", "count": u_count, "percent": ((u_count / total) * 100)}
    letter_list.append(u_dict)

    v_count = letter_input.count("v")
    v_dict = {"letter": "v", "count": v_count, "percent": ((v_count / total) * 100)}
    letter_list.append(v_dict)

    w_count = letter_input.count("w")
    w_dict = {"letter": "w", "count": w_count, "percent": ((w_count / total) * 100)}
    letter_list.append(w_dict)

    x_count = letter_input.count("x")
    x_dict = {"letter": "x", "count": x_count, "percent": ((x_count / total) * 100)}
    letter_list.append(x_dict)

    y_count = letter_input.count("y")
    y_dict = {"letter": "y", "count": y_count, "percent": ((y_count / total) * 100)}
    letter_list.append(y_dict)

    z_count = letter_input.count("z")
    z_dict = {"letter": "z", "count": z_count, "percent": ((z_count / total) * 100)}
    letter_list.append(z_dict)

    return letter_list


def data_center(user_hand, trial, length, counted_letters, user_name):
    total = length

    left = 0
    right = 0
    middle = 0
    table = PrettyTable()
    table.field_names = ["Letter", "Count", "Percentage"]

    for letter in counted_letters:
        table.add_row([letter["letter"], letter["count"], letter["percent"]])
        char = letter["letter"]
        if (
            char == "q"
            or char == "w"
            or char == "a"
            or char == "s"
            or char == "z"
            or char == "x"
            or char == "e"
        ):
            left += letter["count"]
        if (
            char == "d"
            or char == "c"
            or char == "r"
            or char == "f"
            or char == "v"
            or char == "t"
            or char == "g"
            or char == "b"
            or char == "y"
            or char == "h"
            or char == "u"
        ):
            middle += letter["count"]
        if (
            char == "p"
            or char == "o"
            or char == "l"
            or char == "k"
            or char == "m"
            or char == "n"
            or char == "i"
            or char == "j"
        ):
            right += letter["count"]
    left_percent = (left / total) * 100
    middle_percent = (middle / total) * 100
    right_percent = (right / total) * 100

    if (middle_percent > left_percent and middle_percent > right_percent):
        if left_percent > right_percent:
            handedness_message = "* Most of your typing was in the middle of the keyboard, possibly indicating that you are ambidextrous. We estimate you may be left-handed."
            handedness_prediction = "ambidextrous"
        elif right_percent > left_percent:
            handedness_message = "* Most of your typing was in the middle of the keyboard, possibly indicating that you are ambidextrous. We estimate you may be right-handed."
            handedness_prediction = "ambidextrous"
        else:
            pass
    elif right_percent > left_percent:
        handedness_message = "* Based on your inputted letters, we would guess you are right-handed."
        handedness_prediction = "right"

    elif left_percent > right_percent:
        handedness_message = "* Based on your inputted letters, we would guess you are left-handed."
        handedness_prediction = "left"
    else:
        pass

    if handedness_prediction == user_hand:
        correctness = "yes"
    else:
        correctness = "no"

    if trial == 1 or trial == 2 or trial == 3 or trial == 4:
        print(color.CYAN + "\n\n" + handedness_message + color.END)

    trial_dict = {
        "trial": trial,
        "length": total,
        "left_percent": left_percent,
        "middle_percent": middle_percent,
        "right_percent": right_percent,
        "correct": correctness,
        "actual_handedness": user_hand,
        "user_name": user_name,
    }


    return trial_dict, table


def _getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)  # This number represents the length
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def analysis(trials_list):
    """Analyzes the user results and the results of the provided CSV file."""
    correct_new_trials = 0
    incorrect_new_trials = 0
    correct_inp_trials = 0
    incorrect_inp_trials = 0
    correct_right_trials = 0
    correct_left_trials = 0
    incorrect_right_trials = 0
    incorrect_left_trials = 0

    csv_file = input(color.UNDERLINE + "\nEnter your CSV filename (filename.csv) you wish to compare your results with:" + color.END + " ")

    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        inputted_trials = list(reader)

    for trial in trials_list:
        if trial['correct'] == "yes":
            correct_new_trials += 1
            if trial['actual_handedness'] == "right":
                correct_right_trials += 1
            elif trial['actual_handedness'] == "left":
                correct_left_trials += 1
        else:
            incorrect_new_trials += 1
            if trial['actual_handedness'] == "right":
                incorrect_right_trials += 1
            elif trial['actual_handedness'] == "left":
                incorrect_left_trials += 1
            else:
                pass

    for trial in inputted_trials:
        if trial['correct'] == "yes":
            correct_inp_trials += 1
            if trial['actual_handedness'] == "right":
                correct_right_trials += 1
            elif trial['actual_handedness'] == "left":
                correct_left_trials += 1
            else:
                pass
        else:
            incorrect_inp_trials += 1
            if trial['actual_handedness'] == "right":
                incorrect_right_trials += 1
            elif trial['actual_handedness'] == "left":
                incorrect_left_trials += 1
            else:
                pass

    total_correct_trials = correct_inp_trials + correct_new_trials
    total_incorrect_trials = incorrect_new_trials + incorrect_inp_trials
    len_previous_input = len(inputted_trials)
    total = len_previous_input + 4

    new_trial_percent = (correct_new_trials / 4) * 100
    previous_trial_percent = (correct_inp_trials / len_previous_input) * 100
    all_trial_percent = (total_correct_trials / total) * 100

    print(color.UNDERLINE + color.BOLD + color.GREEN + "\n\nRESULTS:" + color.END + color.END + color.END)
    print(color.BOLD + " * Percentage of Correct Trials (4 total trials) from your Run: " + color.END + str(new_trial_percent) + "%")
    print(color.BOLD + " * Percentage of Correct Trials (" + str(len_previous_input) + " total trials) from Imported CSV: " + color.END + str(previous_trial_percent) + "%")
    print(color.BOLD + " * Percentage of Correct Trials (" + str(total) + " total trials) Overall: " + color.END + str(previous_trial_percent) + "%")

def user_input():
    start_time = time.time()
    dataset = []
    print("* BE READY TO TYPE LETTERS IN 5 SECONDS *")

    while time.time() - start_time < 1:
        pass

    print(
        color.BOLD
        + color.RED
        + "\n\n****** START TYPING LETTERS NOW ******\n"
        + color.END
        + color.END
    )
    while time.time() - start_time < 5:
        inputted = _getch()
        dataset.append(inputted)

    return dataset


main()
