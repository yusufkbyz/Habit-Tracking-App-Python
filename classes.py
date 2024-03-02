"""This module has the habit class and handles habit creation."""

class Habits:
    """A class that handles habit creation & aids with migration to sql database.

    Attributes:
    id: habit identification number.
    habit: the habit itself.
    period: the period of which the habit is to be tracked.
    streak: the streak of how long the habit has been completed.
    complete: whetehr the habit is completed for the day/week/month or not.
    date_created: the date of when the habit was created.
    time_created: the time of when the habit was created.
    top_streak: the top streak of the habit's lifetime.
    last_date: the last date of when the habit was checked off.

    Methods:
    None
    """
    def __init__(self, id, habit, period, streak, complete, date_created=None, time_created=None, top_streak=0, last_date='nil'):
        """Initialise the habit tracker with values based on the input."""
        self.id = id
        self.habit = habit
        self.period = period
        self.streak = streak
        self.complete = complete
        self.date_created = date_created
        self.time_created = time_created
        self.top_streak = top_streak
        self.last_date = last_date


class Logs:
    """A class that handles log creation & aids with migration to sql database.

    Attributes:
    id: log identification number.
    habit: the habit itself.
    date_action: the date of when the action took place.
    time_action: the time of when the action took place.
    action: action that took place, eg. deletion.

    Methods:
    None
    """
    def __init__(self, id, habit, date_action, time_action, action):
        """Initialise the logger with values based on the input."""
        self.id = id
        self.habit = habit
        self.date_action = date_action
        self.time_action = time_action
        self.action = action