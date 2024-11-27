import os
from supabase import create_client, Client

# Получение переменных окружения
SUPABASE_URL = os.getenv('NEXT_PUBLIC_SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('NEXT_PUBLIC_SUPABASE_ANON_KEY')

# Создание клиента Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
