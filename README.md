# Project Title
Habit Tracking Application in Python

## Description
This project is a habit tracking app made in python. It handles habit creation, processing and analysis. It stores data locally in your device so that the data can be used across sessions.

## Installation
This project was built in python.

1. Install the relevant libraries: <br>
    `pip install pytest`

2. Navigate to the "main.py" file,

3. Run the file.

## Usage
After you run the main file, follow the instructions displayed in the terminal. 

## Features
Habit creation
* Users have the ability to create habits to follow on a daily/weekly/monthly basis.

Checking off habits
* Users can check off habits once they've fulfilled them
* Users can not check off habits multiple times per period
* A streak value will be appended each time the user checks off a habit
* If a habit has not been checked off after twice the period has passed, the streak will reset to 0.

Deleting habits
* Users have the ability to delete habits from the application.

Analytics module
* Users can opt to analyse several features of their habit tracking journey, which include the following: <br>
    List of all currently tracked habits, <br>
    List of all habits with the same period, <br>
    Longest streak of all habits, <br>
    Longest streak of a certain habit.

Logging Module
* All major habit changes are logged and stored.

## License
[MIT](https://choosealicense.com/licenses/mit/)