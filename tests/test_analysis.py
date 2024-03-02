"""This module tests everything within the analytics function."""

import pytest
from unittest.mock import MagicMock
from analysis import analytics


@pytest.fixture
def mock_cursor_nx():
    """Creates a pytest fixture of a mock cursor. Used throughout a few functions.

    Parameters:
    None

    Returns:
    Mock cursor without any mock executions.
    """
    mock_cur = MagicMock()  # initiating the mock cursor
    mock_cur.fetchall.return_value = [  # storing the defined value when the fetchall function is called in the code
        (1, 'Study', 'daily', 5, 0, '2023-01-15', '10:00:00', 6, '2024-02-01'),
        (2, 'Work Out', 'daily', 6, 0, '2023-01-15', '10:01:00', 7, '2024-02-01'),
        (3, 'Pay Bills', 'monthly', 3, 0, '2023-01-15', '10:02:00', 4, '2024-02-01')
    ]

    return mock_cur


@pytest.fixture
def mock_cursor_3():
    """Creates a pytest fixture of a mock cursor to be used for option 3.

    Parameters:
    None

    Returns:
    Mock cursor.
    """
    mock_cur = MagicMock()
    mock_cur.execute.return_value = None  # execute doesn't need a return value
    mock_cur.fetchall.return_value = [
        (2, 'Work Out', 'daily', 6, 0, '2023-01-15', '10:01:00', 7, '2024-02-01')
    ]

    return mock_cur


@pytest.fixture
def mock_cursor_4():
    """Creates a pytest fixture of a mock cursor to be used for option 4.

    Parameters:
    None

    Returns:
    Mock cursor.
    """
    mock_cur = MagicMock()
    mock_cur.execute.return_value = None
    mock_cur.fetchall.return_value = [
        (1, 'Study', 'daily', 5, 0, '2023-01-15', '10:00:00', 6, '2024-02-01')
    ]

    return mock_cur


@pytest.fixture
def mock_input_1(monkeypatch):
    """Creates a pytest fixture of a mock input to be used for option 1.

    Parameters:
    monkeypatch: built-in fixture under pytest

    Returns:
    None
    """
    inputs = iter(['1', '5'])  # iterates through the defined values
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))  # goes through the inputs when an input is called


@pytest.fixture
def mock_input_2(monkeypatch):
    """Creates a pytest fixture of a mock input to be used for option 2.

    Parameters:
    monkeypatch: built-in fixture under pytest

    Returns:
    None
    """
    inputs = iter(['2', 'daily', '5'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))


@pytest.fixture
def mock_input_3(monkeypatch):
    """Creates a pytest fixture of a mock input to be used for option 3.

    Parameters:
    monkeypatch: built-in fixture under pytest

    Returns:
    None
    """
    inputs = iter(['3', '5'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))


@pytest.fixture
def mock_input_4(monkeypatch):
    """Creates a pytest fixture of a mock input to be used for option 4.

    Parameters:
    monkeypatch: built-in fixture under pytest

    Returns:
    None
    """
    inputs = iter(['4', '1', '5'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))


@pytest.fixture
def mock_print(monkeypatch):
    """Creates a pytest fixture of a mock print. Used throughout most functions.

    Parameters:
    monkeypatch: built-in fixture under pytest.

    Returns:
    List of each print statement called.
    """
    prints = []  
    monkeypatch.setattr('builtins.print', prints.append)  # appends the prints list each time a statement is printed
    
    return prints


def test_analytics_o1(mock_cursor_nx, mock_input_1, mock_print):
    """Tests the functionality of the first analytics feature (all tracked habits)

    Parameters:
    mock_cursor_nx: Mock cursor for database operations.
    mock_input_1: Mock input made for option 1.
    mock_print: Mock print for comparison during assertion.

    Returns:
    Test result.
    """
    analytics(mock_cursor_nx, [])  # executes the function with the mocked cursor and user input
    expected_output = [  # defines the expected output for assertion
        '\nBelow is the list of Habits that are being tracked.',
        '1 | Daily | Streak: 5 | Study |',
        '2 | Daily | Streak: 6 | Work Out |',
        '3 | Monthly | Streak: 3 | Pay Bills |'
    ]
    relevant_print = mock_print[6:10]  # stores the relevant part of the print list

    assert relevant_print == expected_output  # compares the actual output vs the expected one


def test_analytics_o2(mock_cursor_nx, mock_input_2, mock_print):
    """Tests the functionality of the second analytics feature (all habits with the same period)

    Parameters:
    mock_cursor_nx: Mock cursor for database operations.
    mock_input_2: Mock input made for option 2.
    mock_print: Mock print for comparison during assertion.

    Returns:
    Test result.
    """
    analytics(mock_cursor_nx, [])
    expected_output = [
        '1 | Period: Daily | Streak: 5 | Habit: Study',
        '2 | Period: Daily | Streak: 6 | Habit: Work Out'
    ]
    relevant_print = mock_print[7:9]

    assert relevant_print == expected_output


def test_analytics_o3(mock_cursor_3, mock_input_3, mock_print):
    """Tests the functionality of the third analytics feature (longest streak of all habits)

    Parameters:
    mock_cursor_3: Mock cursor for database operations made for option 3.
    mock_input_3: Mock input made for option 3.
    mock_print: Mock print for comparison during assertion.

    Returns:
    Test result.
    """
    analytics(mock_cursor_3, [])
    expected_output = [
        '1 | Period: Daily | Top Streak: 7 | Habit: Work Out'
    ]
    relevant_print = [mock_print[7]]

    assert relevant_print == expected_output


def test_analytics_o4(mock_cursor_4, mock_input_4, mock_print):
    """Tests the functionality of the fourth analytics feature (longest streak of a certain habit)

    Parameters:
    mock_cursor_4: Mock cursor for database operations made for option 4.
    mock_input_4: Mock input made for option 4.
    mock_print: Mock print for comparison during assertion.

    Returns:
    Test result.
    """
    analytics(mock_cursor_4, [])
    expected_ouput = [
        '\n1 | Period: Daily | Top Streak: 6 | Habit: Study'
    ]
    relevant_print = [mock_print[8]]

    assert relevant_print == expected_ouput