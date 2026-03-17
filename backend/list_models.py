
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print("No API key found in .env")
else:
    print(f"API Key found: {api_key[:5]}...")
    try:
        genai.configure(api_key=api_key)
        print("Listing available models...")
        with open('models_list.txt', 'w', encoding='utf-8') as f:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    line = f"- {m.name}\n"
                    print(line.strip())
                    f.write(line)
    except Exception as e:
        print(f"Error listing models: {e}")
