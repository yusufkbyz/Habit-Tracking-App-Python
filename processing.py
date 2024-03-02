"""This module covers most data processing that takes place within the habit tracker."""

import datetime as t
from classes import Habits
from test_fixture import logging

def fetch_habits(cursor):
    """Fetches all habits from the database

    Parameters:
    cursor: cursor for linking to database operations.

    Returns:
    all_habits: list of all habits.
    """
    # fetches habits from sql database
    cursor.execute("SELECT * FROM habits")
    rows = cursor.fetchall()

    # puts all habits into a list
    all_habits = []
    for row in rows:
        habit = Habits(*row)
        all_habits.append(habit)

    return all_habits


def period_pass_func(all_habits):
    """Checks whether the period has passed since the user checked off the habit.

    Parameters:
    all_habits: list of all habits.

    Returns:
    period_pass_list: list of whether the period has passed since the last time the habit was checked off
    period_pass_listx2: list of whether twice the period has passed since the last time the habit was checked off (in order to reset the streak)
    """
    # pre-defining variables
    period_pass_list = []
    period_pass_listx2 = []

    for habit in all_habits:
        # assigning the right value for the comparison
        current_date = t.datetime.now().date()
        if habit.last_date == 'nil':
            habit_date = t.datetime.strptime(habit.date_created, '%Y-%m-%d').date()  # creaitng a date type object
        else:
            if isinstance(habit.last_date, str):
                habit_date = t.datetime.strptime(habit.last_date, '%Y-%m-%d').date()
            else:
                habit_date = habit.last_date

        # checking if the period has passed since the habit was created
        if habit.period.lower() == 'daily':
            period_passed = (current_date - habit_date).days >= 1
            period_passedx2 = (current_date - habit_date).days >= 2
        elif habit.period.lower() == 'weekly':
            period_passed = (current_date - habit_date).days >= 7
            period_passedx2 = (current_date - habit_date).days >= 14
        elif habit.period.lower() == 'monthly':
            period_passed = (current_date.year, current_date.month) > (habit_date.year, habit_date.month)
            period_passedx2 = (current_date.year, current_date.month) > (habit_date.year, habit_date.month + 1)
        else:
            period_passed = False
            period_passedx2 = False
        period_pass_list.append(period_passed)
        period_pass_listx2.append(period_passedx2)

    return period_pass_list, period_pass_listx2


def auto_uncheck(cursor, all_habits, period_pass_list, period_pass_listx2, cursor_l):
    """Makes the user able to check off the habit again once the period has passed & updates the database

    Parameters:
    cursor: cursor of the habits database.
    all_habits: list of all habits.
    period_pass_list: list of whether the period has passed since the last time the habit was checked off
    period_pass_listx2: list of whether twice the period has passed since the last time the habit was checked off (in order to reset the streak)
    cursor_l: cursor of the logging database.

    Returns:
    None
    """
    # pre-definiting iteration variable
    i = 0

    for habit in all_habits:
        # only processing habits that have been checked off recently
        if habit.complete == True:
            if period_pass_list[i] == True:
                # resetting the complete option
                habit.complete = False

                # updating the database
                cursor.execute(
                    '''
                    UPDATE habits
                    SET complete = ?
                    WHERE id = ?
                    ''',
                    (habit.complete, habit.id)
                )

            # updating the top_streak variable if it has been passed
            if habit.top_streak < habit.streak:
                habit.top_streak = habit.streak

            cursor.execute(
                '''
                UPDATE habits
                SET top_streak = ?
                WHERE id = ?
                ''',
                (habit.top_streak, habit.id)
            )

        # checking if double the period has passed since last check off
        if period_pass_listx2[i] == True and habit.streak != 0:
            # resetting the streak
            habit.complete = False
            if habit.top_streak < habit.streak:
                habit.top_streak = habit.streak
            habit.streak = 0
            cursor.execute(
                '''
                UPDATE habits
                SET complete = ?,
                    streak = ?,
                    top_streak = ?
                WHERE id = ?
                ''',
                (habit.complete, habit.streak, habit.top_streak, habit.id)
            )
            # logging the changes
            logging(cursor_l, habit.habit, 'reset')
        # iteration variable
        i += 1


def process(cursor, h_list, p_list):
    """Processes the data from the creation function and puts it into the database.

    Parameters:
    cursor: cursor for linking to database operations.
    h_list: list of habits from the creation function.
    p_list: list of periods of the habits from the creation function.

    Returns:
    all_habits: list of all currently tracked habits.
    """
    # pre-defining empty habits list
    all_habits = []

    # inputting the creation data into the database
    for i in range(len(h_list)):
        immediate_date = t.datetime.now().date()
        immediate_time = t.datetime.now().strftime('%H:%M:%S')
        insert_habit(cursor, h_list[i], p_list[i], 0, False, immediate_date, immediate_time)
    
    # fetching the revised data and putting it into a list
    all_habits = fetch_habits(cursor)

    return all_habits


def insert_habit(cursor, habit, period, streak=0, complete=False, date_created=None, time_created=None, top_streak=0, last_date='nil'):
    """Inserts a habit into the database.

    Parameters:
    cursor: cursor for linking to database operations.
    habit: the habit itself.
    period: the period of which the habit is to be tracked.
    streak (optional): the streak of how long the habit has been completed.
    complete (optional): whetehr the habit is completed for the day/week/month or not.
    date_created (optional): the date of when the habit was created.
    time_created (optional): the time of when the habit was created.
    top_streak (optional): the top streak of the habit's lifetime.
    last_date (optional): the last date of when the habit was checked off.

    Returns:
    None
    """
    # setting a default date if none is provided
    date_created = date_created or t.datetime.now().strftime('%Y-%m-%d')
    time_created = time_created or t.datetime.now().strftime('%H:%M:%S')

    # inserting data into the database
    cursor.execute(
        '''
        INSERT INTO habits (
            habit, period, streak, complete, date_created, time_created, top_streak, last_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        (habit, period, streak, complete, date_created, time_created, top_streak, last_date)
    )


def strike_through(string):
    """Strikes through any given string for display purposes.

    Parameters:
    string: any string

    Returns:
    output: striked-through string
    """
    output = ''
    for i in string:
        output = output + i + '\u0336'

    return output


def delete(cursor, all_habits, n, cursor_l=None):
    """Deletes a habit from the database.

    Parameters:
    cursor: cursor for linking to database operations.
    all_habits: list of all habits.
    n: index number of the habit to be deleted.
    cursor_l (optional): cursor of the logging database.

    Returns:
    new_habits: list of all habits minus the deleted habit.
    """
    # fetching the habit id via the index
    habit_id = all_habits[n - 1].id

    # logging the changes
    if cursor_l == None:
        None
    else:
        logging(cursor_l, all_habits[n - 1].habit, 'delete')

    # deleting the habit from the database
    cursor.execute(
        '''
        DELETE FROM habits
        WHERE id = ?
        ''',
        (habit_id,)
    )

    # fetch the new habits list from the database
    new_habits = fetch_habits(cursor)

    return new_habits

def check_off(cursor, all_habits, n, period_passed, cursor_l=None):
    """Checks off a habit & updates several variables in the database.

    Parameters:
    cursor: cursor for linking to database operations.
    all_habits: list of all habits.
    n: index number of the habit to be deleted.
    period_pass: boolean of whether the period has passed since the last time the habit was checked off
    cursor_l (optional): cursor of the logging database.

    Returns:
    new_habits: list of all habits with the updated entries.
    """
    # handles all input variations
    if isinstance(all_habits, list):
        habit = all_habits[n - 1]
        period_check = period_passed[n - 1]
    else:
        habit = all_habits
        period_check = period_passed

    # checking if the habit has already been completed for the current period
    if habit.complete:
        print("\nThis habit has already been checked off for the current period.")
        return all_habits
    else:
        # handling the possible situation of the user checking off the habit before the period passes
        if period_check == False and habit.complete == True:
            print("\nYou can't check off this habit before the specified period passes.")
        else:
            # updating variables & the database
            habit.complete = True
            habit.streak += 1
            habit.last_date = t.datetime.now().date()
            habit_id = habit.id
            cursor.execute(
                '''
                UPDATE habits
                SET complete = ?, 
                    streak = ?,
                    last_date = ?
                WHERE id = ?
                ''',
                (habit.complete, habit.streak, habit.last_date, habit_id)
            )
            # logging the changes
            if cursor_l == None:
                None
            else:
                logging(cursor_l, habit.habit, 'check off')
        
            # fetch the new habits list from the database
            new_habits = fetch_habits(cursor)

            return new_habits