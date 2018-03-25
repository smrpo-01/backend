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
manage.py dumpdata > data_dump.json
manage.py loaddata data_dump.json
```

## JWT avtentikacija
Na /login/

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


mutation Mutate {
  createTeam(teamData: {
      name: "test1", 
      kmId: 25, 
      poId: 28, 
      members: [
                {id: 25, roles: [3,4]},
                {id: 28, roles: [2]},
        				{id: 27, roles: []}
                ]}) {
    ok
    team{
    	id
      kanbanMaster {
        id
      }
      productOwner {
        id
      }
      members{
        email
      }
      
    }
  }
}

// poId in kmId optional (če v memberjih tega ne spreminjaš)
// po tem ukazu more met team pravilno število memberjev (1 km, 1 pm, >0 dev)
mutation Mutate {
	editTeam(teamData: 
    {teamId: 13, poId: 43, kmId: 40, 
      members: [
        {id: 43, roles: [2]}, 
        {id: 40, roles: [3,4]}, 
        {id:41, roles: [4] }
      ]})
  {
    ok
    team {
      id
    }
  }
}

// deactivira userja
mutation Mutate {
  deleteUserTeam(userTeamId: 46) {
    ok
    team {
      id
    }
  }
}


```
