from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

stores = []
users = []
items = []

class User(BaseModel):
    userName: str
    password: str

class Store(BaseModel):
    id: str
    name: str
    items: List[str] = []

class Item(BaseModel):
    id: str
    name: str
    price: float
    store_id: str

@app.get('/')
def  read_root():
    return {"Bienvenido": "Bienvenido a a la API prueba tecnica"}
    
@app.get('/stores')
def get_store():
    return stores

@app.post('/store/{store_name}')
def create_store(store_name:str, store_temp: Store):       
    store_temp.id = len(stores) + 1
    store_temp.name = store_name
    stores.append(store_temp.dict())
    return store_temp

@app.get('/store/{store_name}')
def view_new_store(store_name: str):
    for store in stores:
        if store["name"] == store_name:
            return store
    return "La tienda no se encuentra registrada"

@app.delete('/store/{store name}')
def delete_store(store_name: str):
    for store in stores:
        if store["name"] == store_name:
            stores.remove(store)
            return "Tienda eliminada"
    return "La tienda no existe"

@app.post('/register')
def save_user(user: User):
    users.append(user.dict())
    return {"message": "User created succesfully."}
    
@app.get('/users')
def get_users():
    return users

@app.post('/auth')
def login(user_login: User):
    for user in users:
        if user["userName"] == user_login.userName and user["password"] == user_login.password :
            return "Login sussesfully"
    return "access_token not found"
    
@app.post('/item/{item_name}')
def create_new_item(item_name: str, item: Item):
    for store in stores:
        if store["id"] == int(item.store_id):
            item.id = len(items) + 1
            item.name = item_name
            items.append(item.dict())
            store["items"] = item
            return store
    return "La tienda no se encuentra registrada"

@app.get('/items')
def get_items():
    return items

@app.put('/item/{item_name}')
def update_item(item_update: Item, item_name: str):
    for item in items:
        if item["name"] == item_name:
            item["price"] = item_update.price
            item["store_id"] = item_update.store_id
            return item
    return "no existe el item"

@app.delete('/store/{item_name}')
def delete_item(item_name: str, item: Item):
    for item_temp in items:
        if item_temp["name"] == item_name:
            items.remove(item_temp)
            return "Item deleted"
    return "El item no existe"