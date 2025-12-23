from fastapi import FastAPI

app = FastAPI(
    title="Risk-Aware ML System",
    description="Ingestion service (skeleton)",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}
