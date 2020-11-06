# QAZPLM

The QAZPLM Program demonstrates hidden biases in the inferences made by larger scale algorithms. It does this, indirectly, by asking users to enter as many random letters on their keyboard during four 15-second trials. The program then summarizes the results from each trial, determining what portion of a user's keystrokes were on the left, middle, or right side of the keyboard. With this, the computer then makes an inference regarding what handedness the user is.

## Running The Program

To run the QAZPLM program, first ensure that Python3 is installed on your system. You can then run the program using Pip or Pipenv depending on your preferences and what you have installed.

### Pipenv

The project comes with a `Pipfile` in the `src` directory that will install the necessary packages for the program, making it easy for users with Pipenv to run the project on their machines.

First navigate to the `src` directory using `cd src`. Then run the command `pipfile lock` to install the necessary Python packages.

You can then run the command `pipenv run python3 qazplm.py` to run the program.

### Pip/Python3

If you have Pip and Python3 installed on your machine, you can use Pip to install the necessary dependencies.

Run the command `pip install prettytable`. Then navigate to the `src` directory and run `python3 qazplm.py` to run the program.


#### Other Packages

The other packages used by this program are `thermios, sys, tty, csv, random, time, threading`. If you encounter errors try to `pip install` these.
