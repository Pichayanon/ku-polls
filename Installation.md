## Instructions for how to install and configure application

> If you use the code below and find ***python : command not found***, change from **python** to **python3**.

1. Clone repository from GitHub to your computer.
    ```
    git clone https://github.com/Pichayanon/ku-polls.git
    ```
2. Change directory to ku-polls.
    ```
    cd  ku-polls
    ```
3. Create virtual environment.
    ```
   python -m venv venv
   ```
4. Start the virtual environment.
   * macOS / Linux
     ```
     . venv/bin/activate 
     ```
   * Windows
     ```
     . .\venv\Scripts\activate
     ```
5. Install dependencies.
   ```
   pip install -r requirements.txt
   ```
6. Set values for externalized variables.
   * macOS / Linux
     ```
     cp sample.env .env 
     ```
   * Windows
     ```
     copy sample.env .env
     ```
7. Run migrations.
   ``` 
   python manage.py migrate
   ```
8. Run test.
   ``` 
   python manage.py test polls
   ```
9. Install data from the data fixtures.
   ``` 
   python manage.py loaddata data/users.json data/polls.json
   ```

   
