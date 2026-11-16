from fastapi import FastAPI

app =FastAPI(
    title="Cloud File Storage",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return{
        "status":"healthy",
        "application":"Cloudfile Storage"
    }