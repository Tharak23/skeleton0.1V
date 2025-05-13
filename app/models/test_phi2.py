from phi2_model import generate_game_logic
import json

def test_phi2_model():
    """Test if the Phi-2 model works correctly"""
    try:
        # Try generating game logic for a simple prompt
        prompt = "Create a simple tic-tac-toe game"
        print(f"Testing Phi-2 model with prompt: '{prompt}'")
        
        # Generate game logic
        game_logic = generate_game_logic(prompt)
        
        # Pretty print the JSON output
        print("Generated game logic JSON:")
        print(json.dumps(game_logic, indent=2))
        
        print("\nPhi-2 model is working correctly!")
        return True
    except Exception as e:
        print(f"Error testing Phi-2 model: {e}")
        print("\nPhi-2 model is NOT working correctly.")
        return False

if __name__ == "__main__":
    test_phi2_model() 