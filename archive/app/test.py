from dotenv import load_dotenv
import os
from supabase import create_client

load_dotenv()  # Load from .env file

url = os.environ['SUPABASE_URL']
key = os.environ['SUPABASE_KEY']

supabase = create_client(url, key)
response = supabase.table("users").select("*").execute()

print(response.data)
