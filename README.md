## Backend

Naj bi blo vse v requirements.txt. Če se da development v venv, da so v 'requirements.txt' samo potrebni.

```
pip freeze > requirements.txt # da dobis requirements

pip install -r requirements.txt # install modules
python manage.py runserver # run server


# Migracije
manage.py makemigrations
manage.py migrate

# brisanje baze
manage.py flush

# Nalaganje/shranjevanje podatkov
# shranjevanje:
python manage.py dumpdata --natural-foreign --exclude auth.permission --exclude contenttypes --indent 4 > data_dump.json
# nalaganje:
manage.py loaddata data_dump.json
```

## Deploy
```
bluemix api https://api.eu-de.bluemix.net/

python manage.py collectstatic --noinput

bluemix login -u <mail> -o smrpo -s emineo
bluemix app push emineo
```

## Mutacije

```
mutation Mutation {
  createUser (userData: {
    email: "test@demo.com",
    password: "demodemo1",
    firstName: "Testni",
    lastName: "Uporabnik",
    roles: [3,4]
  }) {
    user {
      email
      roles {
        name
      }
    }
  }
}

# Za team
QUERIES:

query allTeams {
    teamId -> String || Int
    name -> String
    kanbanMaster -> object {id, firstName, lastName, email, ...}
    productOwner -> object {id, firstName, lastName, email, ...}
    projects -> Array of Project objects {id, naziv, ...}
    developers -> Array of {userId, firstname, lastName, isActive, email}
}


querry allUsers(userRole: !Integer) {
    allUsers(userRole: $userRole) {
        firstName,
        lastName,
        email,
        id
    }
}


MUTACIJE:

// Vsi dodani developerji so aktivni
// kmId in poId se lahko podvoji v primeru da nastopa kot km in developer
mutation addTeam {
    name -> String
    kmId -> Integer (kanban master id)
    poId -> Integer (product owner id)
    developers -> Array of {id: userId (mandatory), email (optional za debagiranje)}
}


// Ne aktivira nobenega uporabnika, vendar lahko doda nove člane
mutation editTeam {
    teamId -> String || Integer (teamId)
    name -> String
    kmId -> Integer (kanban master id)
    poId -> Integer (product owner id)
    developers -> Array of {id: userId (mandatory), email (optional za debagiranje)}
}

mutation editTeamMemberStatus(userTeamId: $id) {
    userTeamId: Integer
    isActive: Boolean
}



mutation Mutate {
  addProject(projectData: 
    {	name: "bla", 
      projectCode: "blabla", 
      dateStart: "2018-5-7", 
      dateEnd: "2018-5-7", 
      customer: "blablabla", 
      teamId: 10, # optional field, če ga ni mi ga ne rabš pošilat
      boardId: 4 # optional field, če ga ni mi ga ne rabš pošilat
    }) {project{id, team {
      id}, board {
        id
      }
    }}
}


```
