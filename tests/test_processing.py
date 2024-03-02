"""This module tests the checking off and deletion functionalities."""

import pytest
from unittest.mock import MagicMock
from processing import check_off, fetch_habits, period_pass_func, delete

@pytest.fixture
def mock_cursor():
    """Creates a pytest fixture of a mock cursor for the tests.

    Parameters:
    None

    Returns:
    Mock cursor.
    """
    mock_cur = MagicMock()  # initiating the mock cursor
    mock_cur.execute.return_value = None  # execute doesn't need a return value
    mock_cur.fetchall.return_value = [  # storing the defined value when the fetchall function is called in the code
        (1, 'Study', 'daily', 5, 0, '2023-01-15', '10:00:00', 6, '2024-02-01'),
        (2, 'Work Out', 'daily', 6, 0, '2023-01-15', '10:01:00', 7, '2024-02-01'),
        (3, 'Pay Bills', 'monthly', 3, 0, '2023-01-15', '10:02:00', 4, '2024-02-01')
    ]

    return mock_cur


@pytest.fixture
def mock_cursor_1():
    """Creates a pytest fixture of a mock cursor for the first test (checking off a habit).

    Parameters:
    None

    Returns:
    Mock cursor.
    """
    mock_cur = MagicMock()  # initiating the mock cursor
    mock_cur.execute.return_value = None  # execute doesn't need a return value
    mock_cur.fetchall.return_value = [  # storing the defined value when the fetchall function is called in the code
        (1, 'Study', 'daily', 5, 0, '2023-01-15', '10:00:00', 6, '2024-02-01'),
        (2, 'Work Out', 'daily', 7, 1, '2023-01-15', '10:01:00', 7, '2024-02-02'),
        (3, 'Pay Bills', 'monthly', 3, 0, '2023-01-15', '10:02:00', 4, '2024-02-01')
    ]

    return mock_cur


@pytest.fixture
def mock_cursor_2():
    """Creates a pytest fixture of a mock cursor for the second test (habit deletion).

    Parameters:
    None

    Returns:
    Mock cursor.
    """
    mock_cur = MagicMock()
    mock_cur.execute.return_value = None
    mock_cur.fetchall.return_value = [
        (1, 'Study', 'daily', 5, 0, '2023-01-15', '10:00:00', 6, '2024-02-01'),
        (3, 'Pay Bills', 'monthly', 3, 0, '2023-01-15', '10:02:00', 4, '2024-02-01')
    ]

    return mock_cur


def test_check_off(mock_cursor, mock_cursor_1):
    """Tests the check_off function.

    Parameters:
    mock_cursor_1: Mock cursor for database operations. 

    Returns:
    Test result.
    """
    # pre-processing variables for expected outputs
    all_habits = fetch_habits(mock_cursor)
    current_streak = all_habits[1].streak
    period_pass_list, period_pass_listx2 = period_pass_func(all_habits)

    # expected output calculation
    checked_off_habit = check_off(mock_cursor_1, all_habits, 2, period_pass_list)
    
    # tests if the expected outputs match with the actual outputs
    assert current_streak + 1 == checked_off_habit[1].streak
    assert checked_off_habit[1].complete == 1


def test_delete(mock_cursor, mock_cursor_2):
    """Tests the delete function.

    Parameters:
    mock_cursor_1: Mock cursor for database operations. Contains all data.
    mock_cursor_2: Mock cursor for database operations. Contains selective data.

    Returns:
    Test result.
    """
    # pre-processing variables for expected outputs
    all_habits = fetch_habits(mock_cursor)
    expected_result = all_habits

    # expected output calculation
    result = delete(mock_cursor_2, all_habits, 2)

    # tests if the expected outputs match with the actual outputs
    assert len(result) == len(expected_result) - 1
    assert result[1].habit == expected_result[2].habit