import uvicorn

if __name__ == "__main__":
    print("Starting AI2D - AI-Powered 2D Game Generator")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 