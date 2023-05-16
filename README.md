## Getting Started

Setup project environment with python -m venv .venv.

```bash
$ git clone https://github.com/ikram9820/utstore.git
$ cd utstore
$ python -m venv .venv

$ .venv/Scripts/activate.ps1               
$ pip install -r requirements.txt

$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py seed_db
$ python manage.py runserver
```
