import os
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from supabase import create_client, Client

app = FastAPI()

def create_supabase_client() -> Client:
    # Создаем клиента Supabase
    supabase_url = os.getenv('NEXT_PUBLIC_SUPABASE_URL')
    supabase_anon_key = os.getenv('NEXT_PUBLIC_SUPABASE_ANON_KEY')

    return create_client(supabase_url, supabase_anon_key)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = JSONResponse(content={"message": "Hello World"})

    # Создаем клиента Supabase
    supabase = create_supabase_client()

    # Управление cookies
    cookie_name = "your_cookie_name"  # Замените на ваше имя cookie
    cookie_value = request.cookies.get(cookie_name, None)

    if cookie_value:
        response.set_cookie(key=cookie_name, value=cookie_value)

    # Установка cookie
    response.set_cookie(key="new_cookie_name", value="new_value", httponly=True)

    # Удаление cookie
    response.delete_cookie(key=cookie_name)

    return response

# @app.get("/")
# async def read_root():
#     return {"Hello": "World"}
