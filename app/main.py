from fastapi import FastAPI

app = FastAPI(title="Reviewass API", version="0.1.0")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def read_root():
    return health_check()
