## Backend

Naj bi blo vse v requirements.txt. Če se da development v venv, da so v 'requirements.txt' samo potrebni.

```
pip3 freeze > requirements.txt # da dobis requirements

pip3 install -r requirements.txt # install modules
python3 manage.py runserver # run server


# Migracije
python3 manage.py makemigrations
python3 manage.py migrate
```
