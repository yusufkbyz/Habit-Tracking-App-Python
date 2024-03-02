"""This module handles a few aspects of the initiation of the habit tracking app."""

def initiate():
    """Prints initialisation messages when the habit tracker is launched.

    Parameters:
    None

    Returns:
    Print statements.
    """
    print('\nWelcome to your Habit Tracker!')
    print('Please provide the following information to get started:')


def sql_table_habit(cursor):
    """Creates the sql table for the habit data if it doesn't exist.

    Parameters:
    cursor: cursor to connect to the sql database.

    Returns:
    None
    """
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit TEXT,
            period TEXT,
            streak INTEGER,
            complete BOOLEAN,
            date_created TEXT,
            time_created TEXT,
            top_streak INTEGER,
            last_date TEXT
        )
        '''
    )


def sql_table_log(cursor_log):
    """Creates the sql table for the logging data if it doesn't exist.

    Parameters:
    cursor_log: cursor to connect to the sql database.

    Returns:
    None
    """
    cursor_log.execute(
        '''
        CREATE TABLE IF NOT EXISTS logging (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit TEXT,
            date_action TEXT,
            time_action TEXT,
            action TEXT
        )
        '''
    )