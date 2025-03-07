from fastapi import FastAPI, HTTPException
from my_extension import MyExtension

app = FastAPI()

# Initialize the extension
extension = MyExtension(app)
extension.setup()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/error")
def cause_error():
    raise HTTPException(status_code=400, detail="An example error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
