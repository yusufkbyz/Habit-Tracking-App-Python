"""This module handles all functions that display """

from processing import strike_through, fetch_habits

def display(all_habits=None, cursor=None):
    """Displays all currently tracked habits.

    Parameters:
    all_habits (optional): list of all currently tracked habits.
    cursor (optional): cursor linked to sql database.

    Returns:
    Print statements.
    """
    # handles all relevant input variations
    if all_habits == None and cursor == None:
        return
    elif cursor == None:
        None
    else:
        all_habits = fetch_habits(cursor)

    # prints all currently tracked habits
    print('\nBelow is the list of Habits that are being tracked.')
    if isinstance(all_habits, list):
        for i in range(len(all_habits)):
            if all_habits[i].complete == False:
                print(f'{i+1} | {all_habits[i].period.capitalize()} | Streak: {all_habits[i].streak} | {all_habits[i].habit} |')
            else:
                print(strike_through(f'{i+1} | {all_habits[i].period.capitalize()} | Streak: {all_habits[i].streak} | {all_habits[i].habit}') + ' | Completed |')
    else:
        if all_habits.complete == False:
            print(f'1 | {all_habits.period.capitalize()} | Streak: {all_habits.streak} | {all_habits.habit} |')
        else:
            print(strike_through(f'1 | {all_habits.period.capitalize()} | Streak: {all_habits.streak} | {all_habits.habit}') + ' | Completed |')


def display_database(cursor):
    """Displays the habit database's raw data.

    Parameters:
    cursor: cursor for linking to database operations.

    Returns:
    Print statements.
    """
    # grabs all habits from the database
    cursor.execute("SELECT * FROM habits")
    rows = cursor.fetchall()

    # prints all habits
    print("\nContents of the habits table:")
    for row in rows:
        print(row)