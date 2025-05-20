import google.generativeai as genai
import os

# Get API key from environment variable
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def list_available_models():
    """
    Lists all available Gemini models and their supported methods.
    """
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY environment variable not set.")
        print("Please set it before running the script.")
        print("Example (in terminal): export GEMINI_API_KEY='YOUR_API_KEY'")
        return

    try:
        # Configure the Gemini client library
        genai.configure(api_key=GEMINI_API_KEY)
        
        print("\nAvailable Gemini Models:")
        print("=======================")
        
        # Get the list of models
        for m in genai.list_models():
            print(f"\nModel: {m.name}")
            print(f"Display name: {m.display_name}")
            print(f"Description: {m.description}")
            print(f"Generation methods: {m.supported_generation_methods}")
            print("-" * 50)
            
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    print("Gemini API Model Lister")
    print("======================")
    print("This script will list all available Gemini models and their capabilities.")
    print("\nMake sure you have:")
    print("1. The 'google-generativeai' library installed")
    print("2. Your GEMINI_API_KEY environment variable set")
    print("\nListing models...\n")
    
    list_available_models() 