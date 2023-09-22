## KU Polls: Online Survey Questions 

[![Django Runtest](https://github.com/Pichayanon/ku-polls/actions/workflows/django-runtest.yml/badge.svg)](https://github.com/Pichayanon/ku-polls/actions/workflows/django-runtest.yml)

An application to conduct online polls and surveys based
on the [Django Tutorial project][django-tutorial], with
additional features.

This app was created as part of the [Individual Software Process](
https://cpske.github.io/ISP) course at Kasetsart University.

## How to Install
Read how to install and configure application from [Installation.md](Installation.md).

## How to Run
1. Activate the virtual environment.
   * macOS / Linux
     ```
     . venv/bin/activate 
     ```
   * Windows
     ```
     venv\Scripts\activate
     ```
2. Starting development server.
    ```
    python manage.py runserver
    ```
    > Note : If you can't use **python**, change it to **python3**.
3. To use the application, open the browser and access http://localhost:8000.
4. To close the application, quit the server with CONTROL-C.
5. Deactivate the virtual environment.
   ```
    deactivate
    ```

## Demo Users
| Username   | Password       |
|------------|----------------|
| demo_user1 | demo_password1 |
| demo_user2 | demo_password2 |

## Project Documents

All project documents are in the [Project Wiki](../../wiki/Home).

- [Vision Statement](../../wiki/Vision-Statement)
- [Requirements](../../wiki/Requirements)
- [Domain Model](../../wiki/Domain-Model)
- [Development Plan](../../wiki/Development-Plan)
- [Iteration 1 Plan](../../wiki/Iteration-1-Plan)
- [Iteration 2 Plan](../../wiki/Iteration-2-Plan)
- [Iteration 3 Plan](../../wiki/Iteration-3-Plan)
- [Iteration 4 Plan](../../wiki/Iteration-4-Plan)
- [Task Board](https://github.com/users/Pichayanon/projects/1)

[django-tutorial]: https://docs.djangoproject.com/en/4.1/intro/tutorial01/