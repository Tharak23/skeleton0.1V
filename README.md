# AI2D - AI-Powered 2D Game Generator (Skeleton Version)

This is the skeleton version of AI2D, which generates simple 2D games from text prompts using local AI models.

## Setup

1. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Install Node.js dependencies:
   ```
   cd frontend
   npm install
   ```

3. Download the Phi-2 model (first run only):
   ```
   python -c "from transformers import AutoModelForCausalLM, AutoTokenizer; model = AutoModelForCausalLM.from_pretrained('microsoft/phi-2', trust_remote_code=True); tokenizer = AutoTokenizer.from_pretrained('microsoft/phi-2', trust_remote_code=True)"
   ```

4. Start the backend:
   ```
   uvicorn app.main:app --reload
   ```

5. Open `frontend/index.html` in your browser.

## Project Structure

- `app/`: FastAPI backend code
- `app/models/`: Phi-2 model integration
- `app/templates/`: Game template code
- `frontend/`: Web UI and Phaser.js game rendering

## How to Use

1. Enter a game description (e.g., "Create a tic tac toe game with space theme")
2. Submit the form
3. Play the generated game in your browser 