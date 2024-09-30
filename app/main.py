from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.utils import comprehensive_research
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)



class ResearchInput(BaseModel):
    query: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the StudyNotion API"}

@app.post("/research")
async def research_endpoint(input: ResearchInput):
    try:
        result = comprehensive_research(input.query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)