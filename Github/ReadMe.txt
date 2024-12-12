Overview:

This project is a Django-based web application designed for XYZ Corporation. It demonstrates data acquisition, storage, and display functionality through a bus reservation system.

Features

User authentication: Sign up, sign in, and logout.
Find buses based on source, destination, and date.
Book and cancel bus tickets.
Admin panel for managing users, buses, and bookings.


The website can be accessed through the following steps: (We have used the jupyter notebook)

1.
import os
import sys
from django.core.management import call_command

# Set the base directory to your project folder
BASE_DIR = "C:/Users/pruth/OneDrive/Desktop/DAP FInal Project/django_apis/djang_brs_updated"  # Update this with the actual path to your project. Following is my directory
sys.path.append(BASE_DIR)

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Initialize Django
import django
django.setup()

2.
call_command('migrate')

3.
import os
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

4.
import os
migration_folder = os.path.join(BASE_DIR, 'myapp', 'migrations')
migration_files = os.listdir(migration_folder)
print(migration_files)

5.
import sqlite3

# Path to your database file
db_path = os.path.join(BASE_DIR, 'db.sqlite3')

# Connect to the database and check tables
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
conn.close()

# Print table names
tables


6.
from django.conf import settings
print(settings.ALLOWED_HOSTS)
print(settings.INSTALLED_APPS)

7.
from django.conf import settings

print("ALLOWED_HOSTS:", settings.ALLOWED_HOSTS)
print("INSTALLED_APPS:", settings.INSTALLED_APPS)
print("DATABASES:", settings.DATABASES)

8.
call_command('runserver', '127.0.0.1:8000')

#If there is any error, we can use %tb and check the error type

Now we can access website with the following ip address:
http://127.0.0.1:8000/