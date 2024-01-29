from models.user_model import usersCreate, UpdatePassword, Update
from fastapi import HTTPException, APIRouter, UploadFile
from dotenv import load_dotenv
from datetime import datetime
from sqlalchemy import text
from instance import engine
from PIL import Image
import hashlib
import psycopg
import os
import jwt
import json

route_user = APIRouter()


# Endpoint : /user/create
# Type : POST
# this endpoint return a new user
# you will need for this endpoint:
# { "firstname":"",
#   "lastname":"",
#    "email":"",
#    "birthdaydate": "DD/MM/YYYY",
#    "address": "",
#    "password": "",
#    "postalcode": "",
#    "age": "",}

@route_user.post("/user/create", response_model=usersCreate)
async def Create(user: usersCreate):
    password_hash = hashlib.md5(
        (user.password + os.getenv('SALT')).encode()).hexdigest()
    query = text("INSERT INTO users (firstname, lastname, email, birthdaydate, address, password, postalcode, age, token, role) VALUES(:firstname, :lastname, :email, :birthdaydate, :address, :password, :postalcode, :age, :token, :role) RETURNING *")
    birthday = datetime.strptime(user.birthdaydate, "%d/%m/%Y").isoformat()
    values = {
        "firstname": user.firstname,
        "lastname": user.lastname,
        "email": user.email,
        "birthdaydate": birthday,
        "address": user.address,
        "password": password_hash,
        "postalcode": user.postalcode,
        "age": user.age,
        "meta": json.dumps({}),
        "token": hashlib.md5((user.email + user.firstname + user.lastname + os.getenv('SALT')).encode()).hexdigest(),
        "role": user.role,
    }
    with engine.begin() as conn:
        result = conn.execute(query, values)
        new_user = result.fetchone()
        print(values)
        return (values)


# Endpoint : /user/{id_user}
# Type : GET
# this endpoint return a intended user

@route_user.get("/user/{id_user}")
async def get_user(id_user: int):
    query = text(f"SELECT * FROM users WHERE id = :id_user")
    values = {"id_user": id_user}
    with engine.begin() as conn:
        result = conn.execute(query, values)
        response = result.fetchone()  # variable qui récup user
        print(response)
    if response is not None:
        if response.role == "admin":
            return {"firstname": response.firstname, "lastname": response.lastname, "email": response.email,
                    "birthdaydate": response.birthdaydate, "address": response.adress, "postalcode": response.postalcode, "age": response.age, "meta": response.meta, "token": response.token, "role": response.role}
        elif response.role == "user":
            return {"firstname": response.firstname, "lastname": response.lastname, "email": response.email, "age": response.age, "role": response.role}
    else:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

     # (voir l'autorisation)

# Endpoint : /connect
# Type : POST
# this endpoint return a token JWT
# you will need for this endpoint:
# {  "email":"",
#    "password": "",}


@route_user.post("/connect")
async def create_user(user: usersCreate):
    # Récupérer l'utilisateur à partir de son email
    query = text("SELECT * FROM users WHERE email = :email")
    values = {"email": user.email}

    with engine.connect() as conn:
        result = conn.execute(query, values)
        response_user = result.fetchone()

    if response_user is None:
        # Si l'utilisateur n'existe pas, renvoyer une erreur 404
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    # Si l'email existe, comparez les mots de passe
    user_password = user.password + os.getenv('SALT')
    hashed_password = hashlib.md5(user_password.encode()).hexdigest()
    print(response_user)

    if hashed_password == response_user.password:
        # Les mots de passe correspondent, générez un token JWT
        encoded_jwt = jwt.encode(
            {"email": user.email}, os.getenv("SECRET_KEY"))
        return {"token": encoded_jwt}
    else:
        # Le mot de passe est incorrect
        raise HTTPException(status_code=401, detail="Mot de passe incorrect")

# Endpoint : /user/update
# Type : POST
# this endpoint return a update of user or admin
# this endpoint return a new user
# you will need for this endpoint:
# { "firstname":"",
#   "lastname":"",
#    "email":"",
#    "birthdaydate": "DD/MM/YYYY",
#    "address": "",
#    "password": "",
#    "postalcode": "",
#    "age": "",}


@route_user.post("/user/update")
async def update(user: Update):
    query = text("SELECT * FROM users WHERE id = :id;")
    values = {"id": user.id}
    with engine.begin() as conn:
        result = conn.execute(query, values)
        response_user = result.fetchone()
        print(result.fetchone())

    if response_user is not None:
        print(response_user.role)
        if response_user.role == "user":
            birthday = datetime.strptime(
                user.birthdaydate, "%d/%m/%Y").isoformat()
            query = text(
                'UPDATE users SET email= :email, birthdaydate= :birthdaydate, address= :address, postalcode= :postalcode, age= :age WHERE id = :id;')
            values = {
                "id": user.id,
                "email": user.email,
                "birthdaydate": birthday,
                "address": user.address,
                "postalcode": user.postalcode,
                "age": user.age
            }
            with engine.begin() as conn:
                result = conn.execute(query, values)

            raise HTTPException(status_code=200, detail="Valeur modifié")

        elif response_user.role == "admin":
            birthday = datetime.strptime(
                user.birthdaydate, "%d/%m/%Y").isoformat()
            query = text('UPDATE users SET email= :email, firstame= :firstname, lastname= :lastname, role= :role, address= :adress, birthdaydate= :birthdaydate, age= :age WHERE id = :id;')
            values = {
                "id": user.id,
                "email": user.email,
                "firstname": user.firstname,
                "lastname": user.lastname,
                "role": user.role,
                "address": user.address,
                "birthdaydate": birthday,
                "age": user.age
            }
            with engine.begin() as conn:
                result = conn.execute(query, values)

            raise HTTPException(
                status_code=200, detail="Valeur de l'admin modifié")
        else:
            raise HTTPException(status_code=404, detail="Not exist")

    else:
        raise HTTPException(status_code=404, detail="User Not found")


# Endpoint : /user/password
# Type : POST
# this endpoint return a new password
# you will need for this endpoint:
# {  "email":"",
#    "password": "",
#    "new_password": "",
#    "repeat_new_password": ""}

@route_user.post("/user/password", response_model=UpdatePassword)
async def update_password_user(user: UpdatePassword):
    query = text("SELECT * FROM users WHERE email = :email")
    values = {"email": user.email}
    print(values)
    password = hashlib.md5(
        (user.password + os.getenv('SALT')).encode()).hexdigest()
    new_password = user.new_password
    repeat_new_password = user.repeat_new_password

    with engine.begin() as conn:
        result = conn.execute(query, values)
        response = result.fetchone()
        print(response.role)

        if response is not None:
            if password == response.password:
                if new_password == repeat_new_password:
                    repeat_new_password = hashlib.md5(
                        (new_password + os.getenv('SALT')).encode()).hexdigest()
                    new_password = hashlib.md5(
                        (new_password + os.getenv('SALT')).encode()).hexdigest()
                    query = text(
                        'UPDATE users SET password = :password WHERE email = :email')
                    print(new_password)
                    print("email")
                    new_values = {"email": user.email,
                                  "password": new_password}
                    with engine.begin() as conn:
                        result = conn.execute(query, new_values)
                    raise HTTPException(
                        status_code=200, detail="Mot de passe modifié")
                else:
                    raise HTTPException(
                        status_code=404, detail="Les mots de passe sont différents")
            else:
                raise HTTPException(
                    status_code=404, detail="Mot de passe incorrect")
        else:
            raise HTTPException(
                status_code=404, detail="Utilisateur introuvable")


# Endpoint : /upload/{user_id}
# Type : POST
# this endpoint return a profil picture

@route_user.post('/upload/{user_id}')
async def upload_profile_image(user_id: int, file: UploadFile):
    user_exists = True
    if not user_exists:
        raise HTTPException(status_code=404, detail='User not found')
    allowed_extensions = {'jpg', 'png', 'gif'}
    ext = file.API.split('.')[-1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail='Invalid file extension')
    if file.content_type not in ['image/jpeg', 'image/png', 'image/gif']:
        raise HTTPException(status_code=400, detail='Invalid image format')
    if file.file:
        content = await file.read()
        if len(content) > 800 * 800:
            raise HTTPException(
                status_code=400, detail='Image size exceeds 800x800 pixels')
    API = f'assets/picture/profiles/{user_id}.{ext}'
    with open(API.jpg, 'wb') as f:
        f.write(content)

    return {'message': 'Image uploaded successfully'}
