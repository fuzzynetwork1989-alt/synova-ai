import requests
import json

# Example: Using Python to talk to your Synova AI

def chat_with_ai(message, tier="terrestrial"):
    """Send a message to Synova AI API"""
    
    url = "http://localhost:8000/api/chat"
    
    payload = {
        "query": message,
        "tier": tier
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise exception for bad status
        
        result = response.json()
        return result["response"]
        
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Example usage
if __name__ == "__main__":
    print("=== Synova AI API Client ===\n")
    
    # Test different tiers
    questions = [
        "What is the meaning of life?",
        "Tell me a joke",
        "How do I deploy a FastAPI app?"
    ]
    
    tiers = ["terrestrial", "aerial", "celestial"]
    
    for tier in tiers:
        print(f"\n--- {tier.upper()} TIER ---")
        for question in questions:
            response = chat_with_ai(question, tier)
            print(f"Q: {question}")
            print(f"A: {response}\n")
