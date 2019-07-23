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


Database migration
---------------------
Create the minesweeper database and run

manage.py migrate


