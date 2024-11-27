import os
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from supabase import create_client, Client

app = FastAPI()

def create_supabase_client(request: Request) -> Client:
    # Создаем клиента Supabase
    supabase_url = os.getenv('NEXT_PUBLIC_SUPABASE_URL')
    supabase_anon_key = os.getenv('NEXT_PUBLIC_SUPABASE_ANON_KEY')
    
    supabase = create_client(supabase_url, supabase_anon_key)
    
    return supabase

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    # Создаем ответ
    response = JSONResponse(content={"message": "Hello World"})
    
    # Создаем клиента Supabase
    supabase = create_supabase_client(request)

    # Обработка cookies
    cookie_name = "your_cookie_name"  # Замените на ваше имя cookie
    cookie_value = request.cookies.get(cookie_name, None)

    if cookie_value:
        response.set_cookie(key=cookie_name, value=cookie_value)

    return response

# @app.get("/")
# async def read_root():
#     return {"Hello": "World"}
