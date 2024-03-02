"""This module handles all the logging of major changes."""

import datetime as t
from classes import Logs

def logging_process(cursor):
    """Fetches all logs from the database

    Parameters:
    cursor: cursor for linking to database operations.

    Returns:
    all_logs: list of all logs.
    """
    # fetches logs from sql database
    cursor.execute("SELECT * FROM logging")
    rows = cursor.fetchall()

    # puts all logs into a list
    all_logs = []
    for row in rows:
        log = Logs(*row)
        all_logs.append(log)

    return all_logs


def logging_print(cursor):
    """Prints all logs from the database

    Parameters:
    cursor: cursor for linking to database operations.

    Returns:
    Print statements.
    """
    # fetching all_logs list for printing
    all_logs = logging_process(cursor)

    # printing the logs
    print('\nThe following are the logs of the habit tracker:')
    i = 0
    for log in all_logs:
        i += 1
        if log.action == 'create':
            print(f'{i} | Habit \'{log.habit}\' was created on {log.date_action} at {log.time_action}.')
        elif log.action == 'check off':
            print(f'{i} | Habit \'{log.habit}\' was checked off on {log.date_action} at {log.time_action}.')
        elif log.action == 'delete':
            print(f'{i} | Habit \'{log.habit}\' was deleted on {log.date_action} at {log.time_action}.')
        elif log.action == 'reset':
            print(f'{i} | Habit \'{log.habit}\'\'s streak was reset on {log.date_action} at {log.time_action}.')


def display_database_logs(cursor):
    """Displays the logging database's raw data.

    Parameters:
    cursor: cursor for linking to database operations.

    Returns:
    Print statements.
    """
    # grabs all logs from the database
    cursor.execute("SELECT * FROM logging")
    rows = cursor.fetchall()

    # prints all logs
    print("\nContents of the logging table:")
    for row in rows:
        print(row)


def logging(cursor, habit, action, date_created=None, time_created=None):
    """Inputs logging data into the database.

    Parameters:
    cursor: cursor for linking to database operations.
    habit: the habit itself.
    action: the action to be logged.
    date_created (optional): the date of creation of the habit.
    time_created (optional): the time of creation of the habit.

    Returns:
    None
    """
    # setting a default date if none is provided
    date_action = date_created or t.datetime.now().strftime('%Y-%m-%d')
    time_action = time_created or t.datetime.now().strftime('%H:%M:%S')

    # inserting data into the database
    cursor.execute(
        '''
        INSERT INTO logging (
            habit, date_action, time_action, action
        ) VALUES (?, ?, ?, ?)
        ''',
        (habit, date_action, time_action, action)
    )