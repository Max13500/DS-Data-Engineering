from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

# BDD utilisateurs initiale
users_db = [
    {
        'user_id': 1,
        'name': 'Alice',
        'subscription': 'free tier'
    },
    {
        'user_id': 2,
        'name': 'Bob',
        'subscription': 'premium tier'
    },
    {
        'user_id': 3,
        'name': 'Clementine',
        'subscription': 'free tier'
    }
]

# Classe utilisateur pour corps de requête 
class User(BaseModel):
    user_id: Optional[int]=None
    name: str
    subscription: str

my_api = FastAPI(
    title='Users API'
)

# Message de bienvenue
@my_api.get('/')
def get_index():
    return {"greetings" : "Bienvenue dans la base des utilisateurs !"}

# Récupération des users
@my_api.get('/users')
def get_users():
    return users_db

# Récupération d'un user particulier
@my_api.get('/users/{userid:int}')
def get_user(userid):
    for dico_user in users_db:
        if (dico_user['user_id'] == userid) :
            return dico_user
    else:
        return {}

# Récupération du nom d'un user particulier
@my_api.get('/users/{userid:int}/name')
def get_user_name(userid):
    for dico_user in users_db:
        if (dico_user['user_id'] == userid) :
            return dico_user['name']
    else:
        return {}

# Récupération du forfait d'un user particulier
@my_api.get('/users/{userid:int}/subscription')
def get_user_subscription(userid):
    for dico_user in users_db:
        if (dico_user['user_id'] == userid) :
            return dico_user['subscription']
    else:
        return {}

# Ajout d'un user (id auto-incrémenté) et affichage de ce user
@my_api.put('/users')
def put_user(user: User):
    new_id = max(users_db, key=lambda u: u.get('user_id'))['user_id'] + 1
    new_user = { 'user_id':new_id, 'name':user.name, 'subscription':user.subscription}
    users_db.append(new_user)
    return new_user

# Modification d'un user particulier et affichage de ce user
@my_api.post('/users/{userid:int}')
def post_users(user: User, userid):
    try:
        old_user = list(
            filter(lambda x: x.get('user_id') == userid, users_db)
            )[0]

        users_db.remove(old_user)

        old_user['name'] = user.name
        old_user['subscription'] = user.subscription

        users_db.append(old_user)
        return old_user

    except IndexError:
        return {}

# Suppression d'un user particulier et affichage de ce user aec confirmation de suppression
@my_api.delete('/users/{userid:int}')
def post_users(userid):
    try:
        old_user = list(
            filter(lambda x: x.get('user_id') == userid, users_db)
            )[0]

        users_db.remove(old_user)

        return {
            'user': old_user,
            'deleted': True
            }

    except IndexError:
        return {}