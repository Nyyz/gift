GiftMate Django project

Setup (development):

1. Create and activate a Python virtual environment (recommended).

2. Install dependencies (Django):

   python -m pip install -r requirements.txt

   If you don't have a requirements.txt, install Django directly:

   python -m pip install Django

3. Set optional environment variables (recommended):

   # Windows PowerShell
   $env:DJANGO_DEBUG = "True"
   $env:DJANGO_SECRET_KEY = "your-secret-key"
   $env:DJANGO_ALLOWED_HOSTS = "localhost,127.0.0.1"

4. Run migrations and start the dev server:

   python manage.py migrate
   python manage.py runserver

5. Create a superuser:

   python manage.py createsuperuser

Notes:
- Static files are served automatically by the dev server.
- For production, set DEBUG=False and configure a proper SECRET_KEY and ALLOWED_HOSTS.

Switching to PostgreSQL (short guide):

1. Install psycopg (or psycopg2-binary):

   python -m pip install psycopg[binary]

2. Update `DATABASES` in `giftmate_project/settings.py`:

   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_db',
           'USER': 'your_user',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }

3. Run migrations against Postgres and create superuser as usual:

   python manage.py migrate
   python manage.py createsuperuser

Creating a local superuser (dev):

   python manage.py createsuperuser

This project uses SQLite for initial development but is structured so switching to Postgres is straightforward.
