# visit-app

# About the visit-app
This app helps users to create a visit, assign start date and end date to the visit as well as add instructions.

# How to use the app

Setting up

1. Create virtual environment 
	- virtualenv "name_of_virtual_environment" eg. virtualenv venv_visit_app
	- activate virtual evironment: source ./venv_visit_app for example.
	- install dependency packages with this command: pip install -r requirements.txt
    
2. Create database and migrate users with this command
	- python user_migrations.py
	This creates the user and visit models and populates the users models with some dummy user data

3. Run the application
	- python server.py (By now the application is running)

4. To visit the swagger ui/ endpoint
	- http://localhost:5000/api/ui/
