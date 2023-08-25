# DjangoCCvalidator
Python w Django, jQuery, TailwindCSS.
Comes with a preconfigured SQLiteDB.

NOTE: Pillow version 10.0 will throw an error, version 9.5 is used here (used for resizing Product thumbnails and converting to WEBP).

Instructions
1. Clone git repo preferably in a virtual env
2. Install the pip packages with pip install -r requirements.txt
3. CMD into the directory and run python manage.py runserver to start the server
4. Add a few products to cart
5. Click on checkout, and enter credit card details.

Database can be changed to Postgres, there is a comment left in settings.py
If you want to change it, first go to shop/migrations and delete all files except __init__.py
