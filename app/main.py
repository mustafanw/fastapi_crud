from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import user, auth, post, player, income, expense
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

origins = [
    settings.CLIENT_ORIGIN,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, tags=['Auth'], prefix='/api/auth')
# app.include_router(user.router, tags=['Users'], prefix='/api/users')
# app.include_router(post.router, tags=['Posts'], prefix='/api/posts')
app.include_router(player.router, tags=['Players'], prefix='/api/players')
app.include_router(income.router, tags=['Incomes'], prefix='/api/incomes')
app.include_router(expense.router, tags=['Expenses'], prefix='/api/expenses')


@app.get('/api/healthchecker')
def root():
    return {'message': 'Hello World'}
