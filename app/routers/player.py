import os
import uuid
from .. import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response, File, UploadFile, Request
from ..database import get_db
from app.oauth2 import require_user
import shutil

router = APIRouter()



@router.get('/list')
def get_players(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''):
    dynamodb = boto3.resource(
        'dynamodb'
    )
    table_name = 'players'
    table = dynamodb.Table(table_name)
    response = table.scan()
    
    return response.get("Items", "")
    skip = (page - 1) * limit

    players = db.query(models.Player).group_by(models.Player.id).filter(
        models.Player.name.contains(search)).limit(limit).offset(skip).all()
    return {'status': 'success', 'results': len(players), 'players': players}

def save_photo(jersey_number: int, photo: UploadFile):
    upload_folder = f"uploads/{jersey_number}"
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, photo.filename)

    with open(file_path, "wb") as file:
        shutil.copyfileobj(photo.file, file)

import boto3
@router.post('/create', status_code=status.HTTP_201_CREATED)
def create_player(player: schemas.CreatePlayerSchema, db: Session = Depends(get_db)):
    dynamodb = boto3.resource(
        'dynamodb'
    )
    table_name = 'players'
    table = dynamodb.Table(table_name)
    # breakpoint()
    response = table.put_item(Item=player.to_dict())

    return {"Success":"Success"}


    new_player = models.Player(**player.dict())
    db.add(new_player)
    db.commit()
    db.refresh(new_player)

    # Save the photo file
#     if photo:
#         save_photo(player.jersey_number, photo)

    return new_player

def update_dynamodb_item(table_name, key_to_update, update_payload):
    # breakpoint()
    # dynamodb = boto3.resource(
    #     'dynamodb',
    #     aws_access_key_id='AKIAQ3EGUXB4Y3IPCQH2',
    #     aws_secret_access_key='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',
    #     region_name='ap-south-1'
    # )
    dynamodb = boto3.resource(
        'dynamodb'
    )
    table = dynamodb.Table(table_name)

    # Build the UpdateExpression and ExpressionAttributeValues
    update_expression = "SET "
    expression_attribute_values = {}
    expression_attribute_names = {}
    for key, value in update_payload.items():
        attribute_name = f"#{key}"
        update_expression += f"{attribute_name} = :{key}, "
        expression_attribute_values[f":{key}"] = value
        expression_attribute_names[f"#{key}"] = key

    update_expression = update_expression.rstrip(', ')
    # breakpoint()
    # Update the item
    table.update_item(
        Key=key_to_update,
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
         ExpressionAttributeNames=expression_attribute_names,
    )

@router.put('/{jersey_number}')
def update_player(jersey_number: int, player: schemas.CreatePlayerSchema, db: Session = Depends(get_db)):
    # breakpoint()
    table_name = 'players'
    key_to_update = {'jersey_number': jersey_number}
    payload = player.dict()
    payload.pop('jersey_number')
    update_dynamodb_item(table_name, key_to_update, payload)

    return {"Success":"Success"}
    player_query = db.query(models.Player).filter(models.Player.jersey_number == jersey_number)
    updated_player = player_query.first()

    if not updated_player:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f'No player with this jersey_number: {jersey_number} found')
    player_query.update(player.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return updated_player

from boto3.dynamodb.types import TypeDeserializer, TypeSerializer

def deserialize(data):
    # breakpoint()
    data = data.get("Item", "")
    deserializer = TypeDeserializer()
    # breakpoint()
    return {k:deserializer.deserialize(v) for k,v in data.items()}

@router.get('/{jersey_number}')
def get_player(jersey_number: int, db: Session = Depends(get_db)):
    dynamodb = boto3.resource(
        'dynamodb'
    )
    table_name = 'players'
    table = dynamodb.Table(table_name)
    response = table.get_item(
            Key={
                'jersey_number': jersey_number
            }
        )
    return response.get("Item", "")
    
    player = db.query(models.Player).filter(models.Player.jersey_number == jersey_number).first()
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No player with this jersey_number: {jersey_number} found")
    return player


@router.delete('/{jersey_number}')
def delete_player(jersey_number: int, db: Session = Depends(get_db)):
    dynamodb = boto3.resource(
        'dynamodb'
    )
    table_name = 'players'
    table = dynamodb.Table(table_name)

    key_to_delete = {'jersey_number':jersey_number}  # Replace with the actual key of the item

    return {"Success":"Success"}

    # Use the delete_item method
    table.delete_item(Key=key_to_delete)

    player_query = db.query(models.Player).filter(models.Player.jersey_number == jersey_number)
    player = player_query.first()
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No player with this jersey_number: {jersey_number} found')

    player_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
