from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import List
import os
import jwt
from Basemodel.user_model import User, usersCreate, UpdatePassword
from Basemodel.departement_model import Department, AddUserToDepartment
from Basemodel.RequestRH_base import RequestRH, CreateRequestRH, RemoveRequestRH
from Basemodel.user_model import User, usersCreate,  UploadProfilePicture, UpdatePassword
from instance import engine

app = FastAPI()

# Configuration de la base de données et de JWT
DATABASE_URL = f"postgresql://{os.environ.get('DATABASE_USER')}:{os.environ.get('DATABASE_PASSWORD')}@{os.environ.get('DATABASE_HOST')}/{os.environ.get('DATABASE_NAME')}"
SECRET_KEY = "151a4a5e4ac14a04ca8651987b733ad40a3e819bf3e18a11d884269ca1edc696"
ALGORITHM = "HS256"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Fonction pour vérifier si un utilisateur est administrateur
def is_admin(token: str = Depends(user)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload['is_admin']

# Endpoint : /department//{id_departement}/users/add
# Type : POST
# this endpoint add a new user in the group department
#  this endpoint return a token 
# this post must contain an array of user IDs.
# you will need for this endpoint:
# {  "id, user
#    "basemodel: deparment_model"",
#    "basemodel": user_model",

# Endpoint pour ajouter des utilisateurs à un département
@app.post("/departements/{id_departement}/users/add", response_model=DepartmentList)
async def add_users_to_department(id_departement: int, users: List[usersCreate], db: Session = Depends(get_db)):
    # Vérifier si le département existe
    department = db.execute(text("SELECT id FROM department WHERE id = :id_departement"), id_departement)
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    users_added = []
    for user in users:
        # Vérifier si l'utilisateur existe
        existing_user = db.execute(text("SELECT id FROM users WHERE id = :user_id"), user.id)
        if existing_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        # Vérifier si l'utilisateur n'est pas déjà dans le département
        user_in_department = db.execute(text("SELECT user_id FROM department_users WHERE department_id = :id_departement AND user_id = :user_id"), id_departement, user.id)
        if user_in_department is None:
            db.execute(text("INSERT INTO department_users (department_id, user_id) VALUES (:id_departement, :user_id)"), id_departement, user.id)
            db.commit()
            users_added.append(user)
    return {"departments": users_added}

# Endpoint : /department//{id_departement}/users/remove
# Type : POST
# this endpoint remove a user in the group department
# this endpoint return a token 
# this post must contain an array of user IDs.
# you will need for this endpoint:
# {  "id, user
#    "basemodel: deparment_model"",
#    "basemodel": user_model",

# Endpoint pour retirer des utilisateurs d'un departement
@app.post("/departements/{id_departement}/users/remove", response_model=List[User])
async def remove_users_from_department(id_departement: int, users: List[User], is_admin: bool = Depends(is_admin)):
    db = SessionLocal()
    users_removed = []
    # Vérifier si le département existe
    department = db.execute(text("SELECT id FROM department WHERE id = :id_departement"), id_departement).fetchone()
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    for user in users:
        # je verifie si l'utilisateur existe
        existing_user = db.execute(text("SELECT id FROM users WHERE id = :user_id"), user.id).fetchone()
        if existing_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        # je verifie si l'utilisateur est dans le département
        user_in_department = db.execute(text("SELECT user_id FROM department_users WHERE department_id = :id_departement AND user_id = :user_id"), id_departement, user.id).fetchone()
        if user_in_department:
            # Retirer l'utilisateur du groupe
            db.execute(text("DELETE FROM department_users WHERE department_id = :id_departement AND user_id = :user_id"), id_departement, user.id)
            users_removed.append(user)
    db.commit()
    db.close()
    return users_removed


# Endpoint : /department//{id_departement}/users
# Type : GET
# this endpoint retrieve users from a group a user
# this endpoint return a token 
# you will need for this endpoint:
# {  "password
#    "birthday_date"",
#    "address"
#    "postal_code"
#    "meta"
#    "jointure" }
#Endpoint pour recuperer un utilisateur dans un groupe 
@app.get("/departement/{id_departement}")
async def get_users_depart(id_departement: int):
    query = text("SELECT * FROM Departments WHERE id = :id_departement")
    values = {"id_departement": id_departement}
     # Create a database connection and execute the query
    with engine.begin() as conn:
        result = conn.execute(query, values)
        response = result.fetchone()
         # Check if the department exists; if not, raise a 404 error
        if response is None:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
         # Retrieve the user's role from the department
        user_role = response.role
        # Based on the user's role, define different SQL queries
        if user_role == "admin":
            # SQL query for admins
            query = text("SELECT u.id, u.firstname, u.lastname, u.email, u.age, u.role FROM users AS u "
                         "INNER JOIN departments AS gu ON u.id = gu.user_id "
                         "WHERE gu.departement_id = :id_departement")
        elif user_role == "user":
              # SQL query for regular users
            query = text("SELECT u.id, u.firstname, u.lastname, u.email, u.age, u.role FROM users AS u "
                         "INNER JOIN departments AS gu ON u.id = gu.user_id "
                         "WHERE gu.departement_id = :id_departement")
        else:
             # If the user's role is not "admin" or "user", raise a 403 error
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        # Execute the appropriate SQL query to get the users in the department
        with engine.connect() as conn:
            result = conn.execute(query, {"id_departement": id_departement})
            users = result.fetchall()
             # If no users are found, raise a 404 error
            if not users:
                 # Return the list of users in the department
                raise HTTPException(status_code=404, detail="Aucun utilisateur trouvé dans le département")
            return users
