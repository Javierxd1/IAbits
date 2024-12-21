from dotenv import load_dotenv
import os

load_dotenv()

OpenAIApiKey = os.getenv('OpenAI_Api_Key')

if not OpenAIApiKey:
    raise ValueError('No se encontró llave para Open AI')