from models.requestrh_model import CreateRequestRH, RemoveRequestRH
from instance import engine
from fastapi import APIRouter
from sqlalchemy import text
from datetime import datetime
import psycopg
import json


route_rh = APIRouter()

# Endpoint : /rh/msg/add
# Type : POST
# this endpoint return if the HR request was made
@route_rh.post("/rh/msg/add", response_model=CreateRequestRH)
async def CreateRequestRH(request: CreateRequestRH):

    print(datetime.now().isoformat())
    content_item = [{
        "author": request.user_id,
        "content": request.content,
        "date": datetime.now().isoformat()
    }]
    
    query = text("INSERT INTO requestrh (userid, content, registrationdate, visibility, close, lastaction, contenthistory) "
                 "VALUES (:userid, :content, :registrationdate, :visibility, :close, :lastaction, :contenthistory) "
                 "RETURNING *")
    # id_user = User.id
    values = {
        "userid": request.user_id,
        "content": request.content,
        "registrationdate": datetime.now().isoformat(),
        "visibility": "true",
        "close": "false",
        "lastaction": datetime.now().isoformat(),
        "contenthistory": json.dumps(content_item)
    }
    with engine.begin() as conn:
        result = conn.execute(query, values)
        print(result)
        response = result.fetchone()
        print(response)

# Endpoint : /rh/msg/remove
# Type : POST
# this endpoint allows you to close the HR request
@route_rh.post("/rh/msg/remove, response_model = RemoveRequestRH")
async def RemoveRequestRH(RequestRH: RemoveRequestRH):
    visibility = False
    close = False
    query = text('UPDATE RequestRH SET visibility = :visibility, close = :close, delete_date = :delete_date, last_action = :last_action WHERE id = :id')
    values = {
        "id": RequestRH.id,
        "visibility": visibility,
        "close": close,
        "delete_date": RequestRH.Lastaction,
        "last_action": RequestRH.Lastaction
    }


