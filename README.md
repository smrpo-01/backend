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

## JWT
```
# da dobiš token userja - avtentikacija
curl -X POST -d "email=admin@demo.com&password=demodemo1" http://localhost:8000/api-token-auth/
```

## Mutacija

```
mutation Mutation {
  createUser (userData: {
    email:"test@demo.com",
    password:"demodemo1",
    firstName:"Testni",
    lastName:"Uporabnik",
    roles:[3,4]
  }) {
    user {
      email
      roles {
        id
      }
    }
  }
}
```