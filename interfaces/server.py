from fastapi import FastAPI
from datetime import datetime

# ---------------------------------------------------------------------------
# Initialization of API Route to interface with agent 
# https://fastapi.tiangolo.com/
# ---------------------------------------------------------------------------

app = FastAPI()

@app.post("/chat")
def chat(message: str):

    with open(os.path.join("signals", "server", datetime.now() + ".txt"), "w") as f:
        f.write(message)
    
    return True

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=int(args.port))
