"""This module handles the menu looping of the main function."""

import processing as proc
import habit_creation as hab_cr
import displays as dis
import analysis as an
import test_fixture as tst

def menu_loop(conn, cursor, all_habits, conn_l, cursor_l):
    """Menu loop for the main function.

    Parameters:
    conn: sql database connector for the habits.
    cursor: cursor of the habits database.
    all_habits: list of all currently tracked habits.
    conn_1: sql database connector for the logs.
    cursor_l: cursor of the logging database.

    Returns:
    None
    """
    while True:
        # handles no habits exception
        if len(all_habits) >= 1:
            dis.display(all_habits, cursor)
        else:
            print('\nCreate a habit to track it.')
        
        # main menu loop
        print('\nThe following are the features that are available in this version:')
        print('1: Add a Habit | 2: Check a Habit Off | 3: Delete a Habit \n4: Analytics | 5: Test Fixture (Logs) | 6: Raw Database Data \n7: End Session')
        while True:
            # input acknowledgement and validation for the menu
            while True:
                try:
                    resp = int(input('\nPlease type the corresponding number to the desired action.\n'))
                    break
                except ValueError:
                    print('\nPlease type a valid integer.')
            if resp == 1 or resp == 2 or resp == 3 or resp == 4 or resp == 5 or resp == 6 or resp == 7:
                break
            else:
                print('\nPlease type a valid response.')

        # adding an additional habit
        if resp == 1:
            habits_list, periods_list = hab_cr.create(cursor_l, all_habits)
            all_habits = proc.process(cursor, habits_list, periods_list)  # Pass 'cursor' here

        # checking a habit off
        elif resp == 2:
            while True:
                if all_habits == []:
                    print('\nYou are not tracking any habits!')
                    break
                while True:
                    try:
                        resp2 = int(input('\nWhich habit would you like to check off? Please provide the corresponding index number.\n'))
                        break
                    except ValueError:
                        print('\nPlease type a valid integer.')
                if resp2 - 1 in range(len(all_habits)):
                    period_pass_list, period_pass_listx2 = proc.period_pass_func(all_habits)
                    all_habits = proc.check_off(cursor, all_habits, resp2, period_pass_list, cursor_l)
                    break
                else:
                    print('\nPlease type a valid response.')
        
        # deleting a habit
        elif resp == 3:
            while True:
                if all_habits == []:
                    print('\nYou are not tracking any habits!')
                    break
                try:
                    resp3 = int(input('\nPlease enter the index number of the Habit you would like to delete.\n'))
                except ValueError:
                    print('\nPlease input a valid integer.')
                if resp3 - 1 in range(len(all_habits)):
                    all_habits = proc.delete(cursor, all_habits, resp3, cursor_l)
                    break
                else:
                    print('\nPlease enter a valid index number.')
        
        # going into the analytics module
        elif resp == 4:
            if all_habits == []:
                print('\nYou are not tracking any habits!')
            else:
                an.analytics(cursor, all_habits)
        
        # displaying all of the logs
        elif resp == 5:
            tst.logging_print(cursor_l)
            
            # dummy input to help declutter terminal
            input('\nType anything to go back to the main menu:\n')

        # displaying raw database data
        elif resp == 6:
            while True:
                response = input('\nWhich database would you like to view (logs or habits)?\n')
                if response.lower() == 'logs' or response.lower() == 'habits':
                    if response.lower() == 'habits':
                        dis.display_database(cursor)
                    else:
                        tst.display_database_logs(cursor_l)
                    while True:
                        response2 = input('\nWould you like to view another database (y or n)?\n')
                        if response2.lower() == 'y' or response2.lower() == 'n':
                            break
                        else:
                            print('\nPlease input a valid response.')
                    if response2.lower() == 'y':
                        None
                    else:
                        break
                else:
                    print('\nPlease input a valid response.')    

        # exiting and saving the changes made in the habit tracker
        elif resp == 7:
            conn.commit()
            conn.close()
            conn_l.commit()
            conn_l.close()
            break