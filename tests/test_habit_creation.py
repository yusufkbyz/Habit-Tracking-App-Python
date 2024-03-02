"""This module tests the habit creation process."""

import pytest
from habit_creation import create

@pytest.fixture
def mock_input(monkeypatch):
    """Creates a pytest fixture of a mock input.

    Parameters:
    monkeypatch: built-in fixture under pytest

    Returns:
    None
    """
    inputs = iter(['Y', 'Study', 'daily', 'y', 'Work Out', 'daily', 'N'])  # iterates through the relevant inputs
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))  # supplies the inputs when an input is called in the create function


def test_create(mock_input):
    """Tests the create function.

    Parameters:
    mock_cursor: a mock cursor to mock database operations.

    Returns:
    Test result.
    """
    # pre-processing variables for expected outputs
    habit_list, period_list = create()
    e_habit_list = ['Study', 'Work Out']
    e_period_list = ['daily', 'daily']
    
    # tests if the expected outputs match with the actual outputs
    assert habit_list == e_habit_list
    assert period_list == e_period_list