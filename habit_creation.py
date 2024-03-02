"""This module handles habit creation."""

from test_fixture import logging

def create(cursor_l=None, all_habits=None):
    """Creates habits based on user input.

    Parameters:
    cursor_l (optional): cursor for the logging module.
    all_habits (optional): list of all currently tracked habits.

    Returns:
    habit_list: list of all habits that were inputted by the user.
    period_list: list of all periods of the habits that were inputted by the user.
    """
    # pre-defining variables to be used in the function
    response = False  # this is to help with systematically breaking out of the function
    habit_list = []
    period_list = []
    if all_habits == None:  # handling all input variations
        response2 = False
    else:
        response2 = True
        for habit in all_habits:
            habit_list.append(habit.habit)
            period_list.append(habit.period)

    # main loop for the habit creation process
    while True:
        if response == False:
            if response2 == False:
                yn = input('\nWould you like to track a new habit (y/n)?\n')
            else:
                yn = 'y'

            if yn.lower() == 'y':
                # clear the lists before taking new inputs
                habit_list.clear()
                period_list.clear()

                while True:
                    ans1 = input('\nWhich habit would you like to track?\n')
                    habit_list.append(ans1)
                    while True:
                        ans2 = input('\nWould you like to track this habit Daily, Weekly, or Monthly?\n')
                        if ans2.lower() == 'daily' or ans2.lower() == 'weekly' or ans2.lower() == 'monthly':
                            break
                        else:
                            print('\nPlease input a valid response.')
                    period_list.append(ans2)
                    while True:
                        ans3 = input('\nWould you like to add another habit (y/n)?\n')
                        if ans3.lower() == 'y' or ans3.lower() == 'n':
                            break
                        else:
                            print('Please enter a valid response.')
                    if ans3.lower() == 'y':
                        None
                    else:
                        response = True
                        # logging all of the habits created
                        if cursor_l == None:
                            None
                        else:
                            for habit in habit_list:
                                logging(cursor_l, habit, 'create')
                        break
            elif yn.lower() == 'n':
                break
            else:
                print('\nPlease enter a valid response.')
        else:
            response = False
            break

    return habit_list, period_list