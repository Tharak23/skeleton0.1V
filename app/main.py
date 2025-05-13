from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json

from app.models.phi2_model import generate_game_logic
from app.templates.game_generator import generate_game_code

app = FastAPI(title="AI2D - AI-Powered 2D Game Generator")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directories if they don't exist
os.makedirs("app/static/games", exist_ok=True)
os.makedirs("app/static/game_logic", exist_ok=True)  # Directory to store JSON game logic

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates/html")

class GamePrompt(BaseModel):
    prompt: str

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    """Render the form to enter a game prompt"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate_game(prompt: str = Form(...)):
    """Generate a game based on the prompt"""
    try:
        # Step 1: Generate game logic JSON using template-based approach (formerly Phi-2 model)
        game_logic = generate_game_logic(prompt)
        
        if not game_logic:
            return JSONResponse(
                status_code=500,
                content={"error": "Failed to generate game logic", "message": "Template selection failed"}
            )
        
        # Create a unique game ID
        game_id = str(hash(prompt))[:8]
        
        # Step 2: Save the game logic JSON to a file
        json_path = f"app/static/game_logic/{game_id}.json"
        with open(json_path, "w") as f:
            json.dump(game_logic, f, indent=2)
        
        # Step 3: Convert game logic to Phaser.js code
        game_code = generate_game_code(game_logic)
        
        # Step 4: Save the game code to a file
        game_path = f"app/static/games/{game_id}.js"
        with open(game_path, "w") as f:
            f.write(game_code)
        
        # Return the game ID and other data as a properly formatted JSON
        return JSONResponse(
            status_code=200,
            content={
                "game_id": game_id, 
                "game_logic": game_logic,
                "json_path": f"/static/game_logic/{game_id}.json"
            }
        )
    
    except Exception as e:
        # Return a proper error response
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "message": "Failed to generate game with template"}
        )

@app.get("/play/{game_id}", response_class=HTMLResponse)
async def play_game(request: Request, game_id: str):
    """Render the page to play a generated game"""
    # Check if the game file exists
    game_path = f"app/static/games/{game_id}.js"
    if not os.path.exists(game_path):
        raise HTTPException(status_code=404, detail="Game not found")
    
    # Check if the JSON file exists
    json_path = f"app/static/game_logic/{game_id}.json"
    game_logic = None
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            try:
                game_logic = json.load(f)
            except json.JSONDecodeError:
                game_logic = {"error": "Invalid game logic JSON"}
        
    return templates.TemplateResponse("play.html", {
        "request": request, 
        "game_id": game_id,
        "game_logic": game_logic,
        "json_path": f"/static/game_logic/{game_id}.json"
    })

@app.get("/game-logic/{game_id}")
async def get_game_logic(game_id: str):
    """Get the game logic JSON for a specific game"""
    json_path = f"app/static/game_logic/{game_id}.json"
    
    if not os.path.exists(json_path):
        return JSONResponse(
            status_code=404,
            content={"error": "Game logic not found"}
        )
    
    try:
        with open(json_path, "r") as f:
            game_logic = json.load(f)
        
        return JSONResponse(content=game_logic)
    
    except json.JSONDecodeError:
        return JSONResponse(
            status_code=500,
            content={"error": "Invalid JSON format"}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 