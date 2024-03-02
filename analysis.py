"""This module includes the analytics feature along with its sub-features."""

from displays import display
from processing import fetch_habits

def print_menu():
    """Prints the list of features available in the analytics module.

    Parameters:
    None

    Returns:
    Print statements.
    """
    # print statements for analytics menu
    print('\nWhat would you like to view?')
    print('1 | List of all currently tracked habits')
    print('2 | List of all habits with the same period')
    print('3 | Longest streak of all habits')
    print('4 | Longest streak of a certain habit')
    print('5 | Back to main menu')


def intro():
    """Gets the user input for the desired feature.

    Parameters:
    None

    Returns:
    response: the input of the user
    """
    print_menu()
    while True:
        try:
            response = int(input(''))
            break
        except ValueError:
            print('\nPlease input a valid integer.')

    return response


def db_data_fetch(cursor, option, ans=None, habit_id=None):
    """Fetches data from the sql database based on the input.

    Parameters:
    cursor: cursor for linking to database operations.
    option: input for picking which part of the code to run.
    ans (optional): user input from previous functions.
    habit_id (optional): user input from previous functions.

    Returns:
    Depends on the options.
    Option 1 - periodicity_list: list of habits where the period (defined by user input) is the same.
    Option 2 - max_streak_all: the habit(s) with the highest streak recorded.
    Option 3 - max_streak_habit: the highest streak of a habit based on user input.
    """
    if option == 1:
        # fetches habits via sql arguments
        cursor.execute('SELECT * FROM habits WHERE period = ?',
            (ans.lower(),))
        periodicity_list = cursor.fetchall()

        return periodicity_list
    elif option == 2:
        cursor.execute(
            '''
            SELECT * FROM habits 
            WHERE top_streak = (SELECT MAX(top_streak) FROM habits)
            '''
        )
        max_streak_all = cursor.fetchall()

        return max_streak_all
    elif option == 3:
        cursor.execute('SELECT * FROM habits WHERE id = ?',
            (habit_id,)
        )
        max_streak_habit = cursor.fetchall()

        return max_streak_habit


def all_tracked_habits(cursor):
    """Fetches all habit data from the sql database.

    Parameters:
    cursor: cursor for linking to database operations.

    Returns:
    Print statements.
    """
    display(cursor=cursor)


def all_same_periods(cursor):
    """Fetches habit data with the same period from the sql database based on the user input.

    Parameters:
    cursor: cursor for linking to database operations.

    Returns:
    Print statements.
    """
    # getting and validating user input
    while True:
        ans = input('\nWhich periodicity would you like to display? (daily, weekly, monthly)\n')
        if ans.lower() == 'daily' or ans.lower() == 'weekly' or ans.lower() == 'monthly':
            break
        else:
            print('\nPlease input a valid period.')

    # fetches and prints all habits with the same periodicity based on user input
    periodicity_list = db_data_fetch(cursor, 1, ans=ans)
    ind = 1
    if periodicity_list == []:
        print(f'\nYou do not have any {ans} habits.')
    else:
        print('')
        for periodicity in periodicity_list:
            print(f'{ind} | Period: {periodicity[2].capitalize()} | Streak: {periodicity[3]} | Habit: {periodicity[1]}')
            ind += 1


def longest_streak_all(cursor):
    """Fetches habit data with the longest streak of all time from the sql database.

    Parameters:
    cursor: cursor for linking to database operations.

    Returns:
    Print statements.
    """
    # fetches the max streak of all time from the habit data & printing the result
    max_streak_all = db_data_fetch(cursor, 2)
    ind = 1
    print('')
    for max_streak in max_streak_all:
        print(f'{ind} | Period: {max_streak[2].capitalize()} | Top Streak: {max_streak[7]} | Habit: {max_streak[1]}')
        ind += 1


def longest_streak_habit(cursor, all_habits):
    """Fetches the longest streak of a certain habit from habit data from the sql database based on the user input.

    Parameters:
    cursor: cursor for linking to database operations.
    all_habits: list of all currently tracked habits.

    Returns:
    Print statements.
    """
    # getting and validating user input
    while True:
        try:
            display(all_habits, cursor)
            ent = int(input('\nWhich habit would you like to view the top streak of?\n'))
        except ValueError:
            print('\nPlease input a valid integer.')
            continue
        if ent - 1 in range(len(all_habits)):
            break
        else:
            print('\nPlease input a valid index number.')

    # fetching and printing the max streak of the user-picked habit.
    habit_id = all_habits[ent - 1].id
    max_streak_habit = db_data_fetch(cursor, 3, habit_id=habit_id)
    print(f'\n1 | Period: {max_streak_habit[0][2].capitalize()} | Top Streak: {max_streak_habit[0][7]} | Habit: {max_streak_habit[0][1]}')


def analytics(cursor, all_habits):
    """Main function for the analytics module. Loops through the features until the user exits.

    Parameters:
    cursor: cursor for linking to database operations.
    all_habits: list of all habits.

    Returns:
    Print statements.
    """
    # analytics menu
    all_habits = fetch_habits(cursor)
    while True:
        response = intro()
        if response == 1:
            all_tracked_habits(cursor)
        elif response == 2:
            all_same_periods(cursor)
        elif response == 3:
            longest_streak_all(cursor)
        elif response == 4:
            longest_streak_habit(cursor, all_habits)
        elif response == 5:
            break