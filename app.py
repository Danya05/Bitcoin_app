import copy
from database import crud
import fastapi
from fastapi import FastAPI, Query, Body
import database
import pydantic_models
import config

api = FastAPI()


@api.get('/user/{user_id}')
def get_users(user_id: str, query: str | None = None):
    if query:
        return {"item_id": user_id, "query": query}
    return {"item_id": user_id}


@api.put('/user/{user_id}')
def update_user(user_id: int, user: pydantic_models.UserToUpdate = fastapi.Body()):
    return crud.update_user(user).to_dict()


@api.delete('/user/{user_id}')
@crud.db_session
def delete_user(user_id: int = fastapi.Path()):
    crud.get_user_by_id(user_id).delete()
    return True


@api.post('/user/create')
def create_user(user: pydantic_models.UserToCreate):
    return crud.create_user(tg_id=user.tg_ID, nick=user.nick if user.nick else None).to_dict()


@api.get('/get_info_by_user_id/{user_id}')
@crud.db_session
def get_user_info(user_id: int):
    return crud.get_user_info(crud.User[user_id])


@api.get('/get_user_balance_by_id/{user_id}')
@crud.db_session
def get_user_balance_by_id(user_id: int):
    return crud.User[user_id].wallet.balance


@api.get('/get_total_balance')
@crud.db_session
def get_total_balance():
    balance = 0.0
    crud.update_all_wallets()
    for user in crud.User.select()[:]:
        balance += user.wallet.balance
    return balance


@api.get('/users/')
@crud.db_session
def get_users():
    users = []
    for user in crud.User.select()[:]:
        users.append(user.to_dict())
    return users


@api.get('/user_by_tg_id/{tg_id}')
@crud.db_session
def get_user_by_tg_id(tg_id: int):
    user = crud.get_user_info(crud.User.get(tg_ID=tg_id))
    return user


@api.post('/create_transaction/{tg_id}')
@crud.db_session
def create_transaction(tg_id: int, cr_transaction: pydantic_models.CreateTransaction):
    return crud.create_transaction(
        sender=crud.User.get(tg_ID=tg_id),
        amount_btc_without_fee=cr_transaction.amount_btc_without_fee,
        receiver_address=cr_transaction.receiver_address,
        testnet=True
    )


'''

<<<LEARNING>>>
<<<WITHOUT Pony.orm>>>

@api.get('/')
@api.post('/')
@api.put('/')
@api.delete('/')
def index(request: Request):
    return {"Request": [request.method, request.headers]}



fake_database = {'users':[
    {
        "id": 1,
        "name": "Anna",
        "nick": "Anny42",
        "balance": 15300
     },

    {
        "id": 2,
        "name": "Dima",
        "nick": "dimon2319",
        "balance": 160.23
     }
    , {
        "id": 3,
        "name": "Vladimir",
        "nick": "Vova777",
        "balance": 200.1
     }
], }


@api.post('/user/create')
def index(user: pydantic_models.User):
    fake_database['users'].append(user)
    return {'User Created!': user}


@api.put('/user/{user_id}')
def update_user(user_id: int, user: pydantic_models.User = fastapi.Body()):
    for index, u in enumerate(fake_database['users']):
        if u['id'] == user_id:
            fake_database['users'][index] = user
            return user


@api.delete('/user/{user_id}')
def delete_user(user_id: int = fastapi.Path()):
    for index, u in enumerate(fake_database['users']):
        if u['id'] == user_id:
            old_db = copy.deepcopy(fake_database)
            del fake_database['users'][index]
            return {'old_db': old_db,
                    'new_db': fake_database}


@api.get('/get_info_by_user_id/{id:int}')
def get_info_about_user(id):
    return fake_database['users'][id-1]


@api.get('/get_user_balance_by_id/{id:int}')
def get_user_balance(id):
    return fake_database['users'][id-1]['balance']


@api.get('/get_total_balance')
def get_total_balance():
    total_balance: float = 0.0
    for user in fake_database['users']:
        total_balance += pydantic_models.User(**user).balance
    return total_balance


@api.get("/users/")
def get_users(skip: int = 0, limit: int = 10):
    return fake_database['users'][skip: skip + limit]

'''
