"""
Quick setup script for AI-powered recommendations
Helps configure Gemini API key
"""

import os
from pathlib import Path

def setup_gemini_api():
    """Interactive setup for Gemini API key"""
    
    print("="*60)
    print("AI-Powered Recommendations Setup")
    print("="*60)
    print()
    
    # Check if .env exists
    env_path = Path('.env')
    env_example_path = Path('.env.example')
    
    if not env_path.exists():
        if env_example_path.exists():
            print("📋 Creating .env from .env.example...")
            with open(env_example_path, 'r') as f:
                content = f.read()
            with open(env_path, 'w') as f:
                f.write(content)
            print("✓ .env file created")
        else:
            print("⚠ .env.example not found. Creating new .env file...")
            with open(env_path, 'w') as f:
                f.write("# Environment Variables\n")
                f.write("MODEL_WEIGHTS=weights/best.pt\n")
                f.write("GEMINI_API_KEY=\n")
            print("✓ .env file created")
    
    print()
    print("To enable AI-powered recommendations:")
    print()
    print("1. Get your Gemini API key:")
    print("   → Visit: https://makersuite.google.com/app/apikey")
    print("   → Sign in with Google account")
    print("   → Click 'Create API Key'")
    print("   → Copy the API key")
    print()
    print("2. Add API key to .env file:")
    print(f"   → Open: {env_path.absolute()}")
    print("   → Find line: GEMINI_API_KEY=your_gemini_api_key_here")
    print("   → Replace with: GEMINI_API_KEY=your_actual_key")
    print()
    print("3. Restart the backend server:")
    print("   → Press Ctrl+C to stop current server")
    print("   → Run: uvicorn main:app --reload")
    print()
    
    # Check if API key is already set
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('GEMINI_API_KEY', '')
    
    if api_key and api_key != 'your_gemini_api_key_here':
        print("✅ GEMINI_API_KEY is configured!")
        print(f"   Key: {api_key[:10]}...{api_key[-4:]}")
        print()
        print("AI-powered recommendations are ENABLED ✨")
    else:
        print("⚠ GEMINI_API_KEY not configured")
        print()
        print("Without API key:")
        print("  • System will use hardcoded recommendations")
        print("  • Recommendations won't adapt to severity")
        print("  • Limited language quality")
        print()
        print("With API key:")
        print("  • Dynamic, severity-based recommendations")
        print("  • High-quality multilingual support")
        print("  • Personalized treatment suggestions")
    
    print()
    print("="*60)

if __name__ == "__main__":
    setup_gemini_api()
