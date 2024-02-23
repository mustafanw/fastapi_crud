import os
import uuid
from .. import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response, File, UploadFile, Request
from ..database import get_db
from app.oauth2 import require_user
import shutil

router = APIRouter()



@router.get('/list', response_model=schemas.ListPlayerResponse, response_class=schemas.CustomJSONResponse)
def get_players(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''):
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

@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=schemas.PlayerResponse, response_class=schemas.CustomJSONResponse)
def create_player(player: schemas.CreatePlayerSchema, db: Session = Depends(get_db)):
    new_player = models.Player(**player.dict())
    db.add(new_player)
    db.commit()
    db.refresh(new_player)

    # Save the photo file
#     if photo:
#         save_photo(player.jersey_number, photo)

    return new_player

@router.put('/{jersey_number}', response_model=schemas.PlayerResponse, response_class=schemas.CustomJSONResponse)
def update_player(jersey_number: int, player: schemas.UpdatePlayerSchema, db: Session = Depends(get_db)):
    player_query = db.query(models.Player).filter(models.Player.jersey_number == jersey_number)
    updated_player = player_query.first()

    if not updated_player:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f'No player with this jersey_number: {jersey_number} found')
    player_query.update(player.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return updated_player

@router.get('/{jersey_number}', response_model=schemas.PlayerResponse, response_class=schemas.CustomJSONResponse)
def get_player(jersey_number: int, db: Session = Depends(get_db)):
    player = db.query(models.Player).filter(models.Player.jersey_number == jersey_number).first()
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No player with this jersey_number: {jersey_number} found")
    return player


@router.delete('/{jersey_number}', response_class=schemas.CustomJSONResponse)
def delete_player(jersey_number: int, db: Session = Depends(get_db)):
    player_query = db.query(models.Player).filter(models.Player.jersey_number == jersey_number)
    player = player_query.first()
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No player with this jersey_number: {jersey_number} found')

    player_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
