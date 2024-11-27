import os
from supabase import create_client, Client

def create_client() -> Client:
    # Получение переменных окружения
    supabase_url = os.getenv('NEXT_PUBLIC_SUPABASE_URL')
    supabase_anon_key = os.getenv('NEXT_PUBLIC_SUPABASE_ANON_KEY')

    # Создание и возврат клиента Supabase
    return create_client(supabase_url, supabase_anon_key)
