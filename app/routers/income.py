import uuid
from .. import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from ..database import get_db
from app.oauth2 import require_user

router = APIRouter()


@router.get('/', response_model=schemas.ListIncomeResponse)
def get_incomes(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''):
    skip = (page - 1) * limit

    incomes = db.query(models.Income).group_by(models.Income.id).filter(
        models.Income.name.contains(search)).limit(limit).offset(skip).all()
    return {'status': 'success', 'results': len(incomes), 'incomes': incomes}


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.IncomeResponse)
def create_income(income: schemas.CreateIncomeSchema, db: Session = Depends(get_db)):
    player = db.query(models.Player).filter(models.Player.name == income.name).first()
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")
    new_income = models.Income(name_id=player.id, **income.dict())
    db.add(new_income)
    db.commit()
    db.refresh(new_income)
    return new_income

@router.put('/{id}', response_model=schemas.IncomeResponse)
def update_income(id: str, income: schemas.UpdateIncomeSchema, db: Session = Depends(get_db)):
    income_query = db.query(models.Income).filter(models.Income.id == id)
    updated_income = income_query.first()

    if not updated_income:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f'No income with this id: {id} found')
    income_query.update(income.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return updated_income


@router.get('/{id}', response_model=schemas.IncomeResponse)
def get_income(id: str, db: Session = Depends(get_db)):
    income = db.query(models.Income).filter(models.Income.id == id).first()
    if not income:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No income with this id: {id} found")
    return income


@router.delete('/{id}')
def delete_income(id: str, db: Session = Depends(get_db)):
    income_query = db.query(models.Income).filter(models.Income.id == id)
    income = income_query.first()
    if not income:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No income with this id: {id} found')

    income_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
