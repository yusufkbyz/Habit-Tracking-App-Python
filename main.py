"""This module is the main module that runs the habit tracker."""

import sqlite3
import habit_creation as hab_cr
import initiation as ini
import processing as proc
import menu as mn

def main_loop():
    """Combines all of the other modules into the habit tracking app.

    Parameters:
    None

    Returns:
    None
    """
    # initialisation steps
    conn_habit = sqlite3.connect('habits.db')  # connecting the cursor to the habits database 
    cursor_habit = conn_habit.cursor()
    conn_log = sqlite3.connect('logging.db')  # connecting the cursor to the logging database
    cursor_log = conn_log.cursor()  
    ini.sql_table_habit(cursor_habit)
    ini.sql_table_log(cursor_log)
    ini.initiate()
    habits_list, periods_list= hab_cr.create(cursor_log)

    # processing steps
    all_habits = proc.process(cursor_habit, habits_list, periods_list) 
    period_pass_list, period_pass_listx2 = proc.period_pass_func(all_habits)
    proc.auto_uncheck(cursor_habit, all_habits, period_pass_list, period_pass_listx2, cursor_log)

    # main loop
    mn.menu_loop(conn_habit, cursor_habit, all_habits, conn_log, cursor_log)


# runs the main_loop function when the code is run
if __name__ == '__main__':
    main_loop()