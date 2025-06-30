from fastapi import FastAPI
from routers import research
from routers import users
from supabase_client import client

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"]
)

app.include_router(research.router)
app.include_router(users.router)

@app.get("/")
def read_root():
  return {"message": "home route reached"}


@app.get("/test")
def get_test():
  return {"message": "test route reached"}


if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="127.0.0.1", port=8000)
