# The Spotlight (Django App)

The Spotlight is a Django implementation of the thespotlight.gr website.
Developed with with the Django Framework while leveraging other technologies such as jQuery, Markdown, Bootstrap, APIs, and more.

### Installation

Install the dependencies.

```sh
$ sudo apt-get install build-essential libssl-dev libffi-dev libjpeg-dev python-dev python3-dev
```

Install the requirements.

```sh
$ cd thespotlight/
$ pip install -r requirements.txt
```

Make the migrations.

```sh
$ cd src/
$ python manage.py makemigrations && python manage.py migrate
```

Create a superuser.

```sh
$ python manage.py createsuperuser
```

Collect the static files.

```sh
$ python manage.py collectstatic --no-input
```

Start the server.

```sh
$ python manage.py runserver
```

License
----

MIT

**Free Software, Hell Yeah!**