import uuid
from .. import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from ..database import get_db
from app.oauth2 import require_user

router = APIRouter()


@router.get('/', response_model=schemas.ListExpenseResponse)
def get_expenses(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''):
    skip = (page - 1) * limit

    expenses = db.query(models.Expense).group_by(models.Expense.id).filter(
        models.Expense.expense_name.contains(search)).limit(limit).offset(skip).all()
    return {'status': 'success', 'results': len(expenses), 'expenses': expenses}


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ExpenseResponse)
def create_expense(expense: schemas.CreateExpenseSchema, db: Session = Depends(get_db)):

    new_expense = models.Expense(**expense.dict())
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

@router.put('/{id}', response_model=schemas.ExpenseResponse)
def update_expense(id: str, expense: schemas.UpdateExpenseSchema, db: Session = Depends(get_db)):
    expense_query = db.query(models.Expense).filter(models.Expense.id == id)
    updated_expense = expense_query.first()

    if not updated_expense:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f'No expense with this id: {id} found')
    expense_query.update(expense.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return updated_expense


@router.get('/{id}', response_model=schemas.ExpenseResponse)
def get_expense(id: str, db: Session = Depends(get_db)):
    expense = db.query(models.Expense).filter(models.Expense.id == id).first()
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No expense with this id: {id} found")
    return expense


@router.delete('/{id}')
def delete_expense(id: str, db: Session = Depends(get_db)):
    expense_query = db.query(models.Expense).filter(models.Expense.id == id)
    expense = expense_query.first()
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No expense with this id: {id} found')

    expense_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
