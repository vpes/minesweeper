Minesweeper API backend
===========================

author: Victor Pesquin
email: vpesquin@acm.org


Description
--------------

Due the short available time for this development I will choose Python, Django and DRF as language and framework.

I will use PostgreSQL for persistence. I expect to store the game board as a dictionary



Basic Commands
^^^^^^^^^^^^^^

Project configuration
---------------------

The project is cofigured with django-environment

Create an env/env-dev file containing

DJANGO_DEBUG='True'

DATABASE_URL='postgresql://<db_user>:<db_password>@<db_url>:<db_port>/minesweeper'

DJANGO_SECRET_KEY="b&rz6(zm##i85^miw_#kyod#dfj))bovwnc9tlnap$q(=-ef@d" # or any other secret key

I have add a default value for those keys to avoid the environment issue in the command line execution


Virtual environment
-------------------

Create the virtual environment inside the django-API folder. Python3 and pip are required

user@group:<path_to_src_foilder>/django-API$ python3.6 -m venv .venv


Activate the virtual environment

user@group:<path_to_src_foilder>/django-API$ source .venv/bin/activate


Install the dependencies

(.venv)user@group: <path_to_src_foilder>/django-API$ pip install -r requirements.txt



Database migration
------------------

Create the minesweeper database and run

python3 manage.py migrate



Run the project
----------------

Run the development django server (port 8008)

(.venv)user@group: <path_to_src_foilder>/django-API$ python3 manage.py runserver 0.0.0.0:8008



Open the user interface
-----------------------

Open FrontEnd/minesweeper.html in your browser

For debug, uncomment the lines 242 and 243 in js/minesweeper.js and reload the game


Notes
-----

If a started game already exists, this game will be opened instead a new game.

All the required features are done except time tracking.

