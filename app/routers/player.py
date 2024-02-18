import uuid
from .. import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from ..database import get_db
from app.oauth2 import require_user

router = APIRouter()


@router.get('/', response_model=schemas.ListPlayerResponse)
def get_players(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''):
    skip = (page - 1) * limit

    players = db.query(models.Player).group_by(models.Player.id).filter(
        models.Player.name.contains(search)).limit(limit).offset(skip).all()
    return {'status': 'success', 'results': len(players), 'players': players}


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PlayerResponse)
def create_player(player: schemas.CreatePlayerSchema, db: Session = Depends(get_db)):
    new_player = models.Player(**player.dict())
    db.add(new_player)
    db.commit()
    db.refresh(new_player)
    return new_player

@router.put('/{jersey_number}', response_model=schemas.PlayerResponse)
def update_player(jersey_number: int, player: schemas.UpdatePlayerSchema, db: Session = Depends(get_db)):
    player_query = db.query(models.Player).filter(models.Player.jersey_number == jersey_number)
    updated_player = player_query.first()

    if not updated_player:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f'No player with this jersey_number: {jersey_number} found')
    player_query.update(player.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return updated_player


@router.get('/{jersey_number}', response_model=schemas.PlayerResponse)
def get_player(jersey_number: int, db: Session = Depends(get_db)):
    player = db.query(models.Player).filter(models.Player.jersey_number == jersey_number).first()
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No player with this jersey_number: {jersey_number} found")
    return player


@router.delete('/{jersey_number}')
def delete_player(jersey_number: int, db: Session = Depends(get_db)):
    player_query = db.query(models.Player).filter(models.Player.jersey_number == jersey_number)
    player = player_query.first()
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No player with this jersey_number: {jersey_number} found')

    player_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
