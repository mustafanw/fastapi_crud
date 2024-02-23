from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import user, auth, post, player, income, expense
from fastapi.staticfiles import StaticFiles
from mangum import Mangum
app = FastAPI(title="RCC")
# app = FastAPI(
#     openapi_extra={
#         "info": {
#             "title": "Your API Title",
#             "version": "1.0",
#             "description": "Your API description",
#         },
#         "responses": {
#             "200": {
#                 "description": "Success",
#             },
#         },
#     },
# )
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
handler = Mangum(app)

# app.include_router(auth.router, tags=['Auth'], prefix='/api/auth')
# app.include_router(user.router, tags=['Users'], prefix='/api/users')
# app.include_router(post.router, tags=['Posts'], prefix='/api/posts')
app.include_router(player.router, tags=['Players'], prefix='/api/players')
# app.include_router(income.router, tags=['Incomes'], prefix='/api/incomes')
# app.include_router(expense.router, tags=['Expenses'], prefix='/api/expenses')


# @app.get('/api/healthchecker')
# def root():
#     return {'message': 'Hello World'}
from app import schemas
@app.get('/openapi.json', response_class=schemas.CustomJSONResponse)
def get_swagger():
    return app.openapi
