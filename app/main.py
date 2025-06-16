from fastapi import FastAPI
from routers import research

app = FastAPI()
app.include_router(research.router)


@app.get("/")
def read_root():
  return {"message": "home route reached"}


@app.get("/test")
def get_test():
  return {"message": "test route reached"}


if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=8000)
